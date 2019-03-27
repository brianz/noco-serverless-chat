'''Template for a Python3 project on AWS.'''
import json
import boto3
import sys

from noco import aws
from noco.helpers import safe_dumps


def default(event, context):
    """Default handler for websocket messages"""
    message = event.get('body', '')

    if not message.strip():
        return {
            'statusCode': 200,
        }

    if message.startswith('/'):
        return _handle_slash(message, event)

    # Steps to broadcast messages to all connected users. All of the helper functions you need for
    # this exist in the `noco/aws.py` file.
    #
    # 1. Get the user identified by the incoming connection_id from DynamoDB.
    # 2. After you have the user record, save the incoming message to DynamoDB
    # 3. Now that the message is saved to DynamoDB, broadcast that message out to everyone else who
    #    is connected.

    # Get the user from dynamodb

    # Save the message to dynamodb

    # broadcast the message to all connected users

    return {
        'statusCode': 200,
        'body': safe_dumps(message),
    }


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


def _handle_slash(message, event):
    if message.startswith('/name '):
        return _set_name(message, event)

    if message.startswith('/channel '):
        return _set_channel(message, event)

    return _help(message, event)


def _help(event):
    message = "Valid commands: /help, /name [NAME], /channel [CHAN_NAME]"
    _send_message_to_client(event, message)
    return {
        'statusCode': 200,
        'body': 'help',
    }


def _set_name(message, event):
    name = message.split('/name')[-1]
    connection_id = _get_connection_id(event)
    aws.save_username(connection_id, name.strip())

    _send_message_to_client(event, 'Set username to {}'.format(name.strip()))

    return {
        'statusCode': 200,
        'body': 'name',
    }


def _set_channel(message, event):
    channel_name = message.split('/channel')[-1]
    channel_name = channel_name.strip('# ')

    connection_id = _get_connection_id(event)

    aws.update_channel_name(connection_id, channel_name)
    aws.set_connection_id(connection_id, channel=channel_name)

    _send_message_to_client(event, 'Changed to #{}'.format(channel_name))

    return {
        'statusCode': 200,
        'body': 'name',
    }


def _send_message_to_client(event, message):
    client = boto3.client('apigatewaymanagementapi', endpoint_url=_get_endpoint(event))
    client.post_to_connection(
        ConnectionId=_get_connection_id(event),
        Data=message,
    )


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
