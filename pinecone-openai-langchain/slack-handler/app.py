import boto3
import os
import base64
import json
import urllib.parse

client = boto3.client('sns')
#client = boto3.client('sqs')

def parse_slack_payload(data):
    # decode the data using the b64decode function
    decoded_data_raw = base64.b64decode(data).decode('utf-8').split('&')

    decoded_data_formatted={}
    for item in decoded_data_raw:
        data_object = item.split('=')
        decoded_data_formatted[data_object[0]] = data_object[1]
    print(decoded_data_formatted)
    return decoded_data_formatted

def handler(event, context):
    if event['isBase64Encoded']:
        decoded_data_encoded = event["body"]
        data = parse_slack_payload(event["body"])
        msg = urllib.parse.unquote_plus(data['text'])
        response_url = urllib.parse.unquote(data['response_url'])
    body = {'msg': msg, 'response_url': response_url}
    topicARN = os.getenv("topicARN")
    response = client.publish(TopicArn = topicARN, Message = json.dumps(body))
    return {"text":"Received your question, will reply in a minute"}
