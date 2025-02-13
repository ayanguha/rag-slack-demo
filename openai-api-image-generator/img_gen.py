import requests
from openai import OpenAI
import json



def get_image_url(msg):
    client = OpenAI()

    response = client.images.generate(model="dall-e-3",
                                      prompt=msg,
                                      n=1,
                                      quality="standard",
                                      size='1024x1024')
    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    print(revised_prompt)
    return image_url


def post_to_slack(image_url, response_url):
    data = {"text":'', "attachments": [{'text': '', 'image_url': image_url}]}
    print(data)
    resp = requests.post(response_url, json = data)
    print(resp)
    return resp

def handler(event, context):

    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    body = json.loads(message)
    print(body)
    user_msg = body['msg']
    response_url = body['response_url']
    image_url = get_image_url(user_msg)
    resp = post_to_slack(image_url, response_url)
    return {'final': True}
