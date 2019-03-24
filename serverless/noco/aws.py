import os
import boto3
import hashlib
import json
import decimal

# from boto3.dynamodb.conditions import Key
# from botocore.exceptions import ClientError

MESSAGE_TABLE_NAME = os.environ['DYNAMO_TABLE_NAME']

# DynamoDB stuff


def get_dynamodb():    # pragma: no cover
    """Return a dynamodb resource"""
    return boto3.resource('dynamodb')


def get_table(table_name=MESSAGE_TABLE_NAME):    # pragma: no cover
    """Create a dynamodb resource"""
    dynamodb = get_dynamodb()
    return dynamodb.Table(table_name)


def set_connection_id(connection_id, channel='general'):
    """Save an initial connection"""
    table = get_table()

    conn_key = _get_channel_connections_key(channel)
    coll_name = _get_connection_column_name(connection_id)
    update_expr = 'SET {} = :value'.format(coll_name)

    table.update_item(
        Key=conn_key,
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':value': {
                'connection_id': connection_id,
                'channel': channel,
            }
        },
        ReturnValues='UPDATED_NEW',
    )


def delete_connection_id(connection_id, channel='general'):
    """Delete an item from DynamoDB which represents a client being connected"""
    table = get_table()

    conn_key = _get_channel_connections_key(channel)
    coll_name = _get_connection_column_name(connection_id)
    update_expr = 'REMOVE {}'.format(coll_name)

    table.update_item(
        Key=conn_key,
        UpdateExpression=update_expr,
    )


def get_user(connection_id):
    table = get_table()
    key = _get_user_key(connection_id)
    row = table.get_item(Key=key)
    return row.get('Item', key)


def update_channel_name(connection_id, name):
    item = get_user(connection_id)

    old_channel = item.get('channel_name', 'general')
    delete_connection_id(connection_id, old_channel)

    item['channel_name'] = name

    table = get_table()
    table.put_item(Item=item)

    set_connection_id(connection_id, name)


def save_username(connection_id, name):
    update_expr = 'SET username = :value'

    table = get_table()
    table.update_item(
        Key=_get_user_key(connection_id),
        UpdateExpression=update_expr,
        ExpressionAttributeValues={':value': name},
    )


def save_message(connection_id, epoch, message, channel='general'):
    """Save a message from a user"""
    item = {
        'pk': channel,
        'epoch': epoch,
        'connectionId': connection_id,
        'channel': channel,
        'message': message,
    }

    table = get_table()
    table.put_item(Item=item)


def get_connected_connection_ids(channel='general'):
    table = get_table()

    key = _get_channel_connections_key(channel)
    row = table.get_item(Key=key)

    for key, payload in row.get('Item', {}).items():
        if key.startswith('CONN'):
            yield payload['connection_id']


def _get_channel_conn_pk(channel):
    return '%s:::connections' % (channel, )


def _get_channel_message_pk(channel, connection_id):
    return '%s:::%s' % (channel, connection_id)


def _get_channel_connections_key(channel):
    pk = _get_channel_conn_pk(channel)
    return {'pk': pk, 'epoch': 0}


def _get_user_key(connection_id):
    return {'pk': connection_id, 'epoch': 0}


def _get_connection_column_name(connection_id):
    return 'CONN' + hashlib.md5(connection_id.encode()).hexdigest()[:16]


# Lambda stuff


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def invoke_lambda_async(function_name, payload):
    """Invoke a Lambda function with an Event invocation type"""
    _lambda = boto3.client('lambda')
    return _lambda.invoke(
        FunctionName=function_name,
        Payload=json.dumps(payload, cls=DecimalEncoder),
        InvocationType='Event',
    )
