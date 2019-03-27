'''Template for a Python3 project on AWS.'''
import json
import boto3
import sys

from noco import aws


def default(event, context):
    """Default handler for websocket messages"""
    print(event)

    # Steps to send yourself a message
    #
    # 1. Get the message from the event above. Fire up a websocket connection and type some
    #    stuff...see where it shows up in the event by looking at the CloudWatch logs
    # 2. After you know how to get the arriving message, use one of the helper functions
    #    below to send yourself back the same message.

    return {
        'statusCode': 200,
    }


def connect(event, context):
    return {
        'statusCode': 200,
        'body': 'connect',
    }


def disconnect(event, context):
    return {
        'statusCode': 200,
        'body': 'disconnect',
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
