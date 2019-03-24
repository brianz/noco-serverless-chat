'''Template for a Python3 project on AWS.'''
import json
import boto3
import sys

from noco import aws


def default(event, context):
    """Default handler for websocket messages"""
    message = event['body']

    if not message.strip():
        return {
            'statusCode': 200,
        }

    if message.startswith('/name '):
        return _set_name(message, event)

    if message.startswith('/channel '):
        return _set_channel(message, event)

    if message.startswith('/'):
        return _help(event)

    connection_id, request_time = _get_conn_id_and_time(event)

    user = aws.get_user(connection_id)
    channel_name = user.get('channel_name', 'general')
    username = user.get('username', 'anonymous')

    # Save the message to dynamodb
    aws.save_message(connection_id, request_time, message, channel_name)

    # Invoke the broadcast function which will send the new message to all connected clients
    func_name_parts = context.function_name.split('-')[:-1] + ['broadcast']
    broadcast_func_name = '-'.join(func_name_parts)

    aws.invoke_lambda_async(
        broadcast_func_name, {
            'body': message,
            'endpoint': _get_endpoint(event),
            'sender': connection_id,
            'channel': channel_name,
            'username': username,
        })

    return {
        'statusCode': 200,
        'body': json.dumps(message),
    }


def broadcast(event, context):
    message = event['body']
    endpoint = event['endpoint']
    sender = event['sender']
    channel = event['channel']
    username = event['username']

    client = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint)

    # need to look up what channel the user is connected to
    for connection_id in aws.get_connected_connection_ids(channel):
        if connection_id == sender:
            continue

        client.post_to_connection(
            ConnectionId=connection_id,
            Data='{}: {}'.format(username, message),
        )


def connect(event, context):
    connection_id = _get_connection_id(event)
    aws.set_connection_id(connection_id)

    return {
        'statusCode': 200,
        'body': 'connect',
    }


def disconnect(event, context):
    connection_id = _get_connection_id(event)

    user = aws.get_user(connection_id)
    channel_name = user.get('channel_name', 'general')
    aws.delete_connection_id(connection_id, channel_name)

    return {
        'statusCode': 200,
        'body': 'disconnect',
    }


def _help(event):
    client = boto3.client('apigatewaymanagementapi', endpoint_url=_get_endpoint(event))
    message = "Valid commands: /help, /name [NAME], /channel [CHAN_NAME]"
    client.post_to_connection(
        ConnectionId=_get_connection_id(event),
        Data=message,
    )
    return {
        'statusCode': 200,
        'body': 'help',
    }


def _set_name(message, event):
    name = message.split('/name')[-1]
    connection_id = _get_connection_id(event)
    aws.save_username(connection_id, name)

    return {
        'statusCode': 200,
        'body': 'name',
    }


def _set_channel(message, event):
    channel_name = message.split('/channel')[-1]
    channel_name = channel_name.strip()

    connection_id = _get_connection_id(event)

    aws.update_channel_name(connection_id, channel_name)
    aws.set_connection_id(connection_id, channel=channel_name)

    return {
        'statusCode': 200,
        'body': 'name',
    }


def _get_connection_id(event):
    ctx = event['requestContext']
    return ctx['connectionId']


def _get_request_time(event):
    ctx = event['requestContext']
    return ctx['requestTimeEpoch']


def _get_conn_id_and_time(event):
    ctx = event['requestContext']
    return (ctx['connectionId'], ctx['requestTimeEpoch'])


def _get_endpoint(event):
    ctx = event['requestContext']
    domain = ctx['domainName']
    stage = ctx['stage']
    return 'https://{}/{}'.format(domain, stage)
