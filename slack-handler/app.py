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
        if data_object[0] in ['token', 'team_id', 'team_domain',
                              'channel_id', 'channel_name', 'api_app_id',
                              'user_id', 'user_name', 'trigger_id']:
            decoded_data_formatted[data_object[0]] = data_object[1]
        elif data_object[0] in ['command','response_url']:
            decoded_data_formatted[data_object[0]] = urllib.parse.unquote(data_object[1])
        elif data_object[0] in ['text']:
            decoded_data_formatted[data_object[0]] = urllib.parse.unquote_plus(data_object[1])


    print(decoded_data_formatted)

    return decoded_data_formatted

def handler(event, context):
    ragTopicARN = os.getenv("ragTopicARN")
    imageTopicARN = os.getenv("imageTopicARN")
    if event['isBase64Encoded']:
        decoded_data_encoded = event["body"]
        data = parse_slack_payload(event["body"])
        msg = data['text']
        response_url = data['response_url']

    body = {'msg': msg, 'response_url': response_url}
    if data['command'] == '/pinecone-openai-openai':
        topicARN = ragTopicARN
    elif data['command'] == '/image-generation-example':
        topicARN = imageTopicARN
    else:
        print("Unknown command")

    response = client.publish(TopicArn = topicARN, Message = json.dumps(body))
    return {"text":"Received your question, will reply in a minute"}
