import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from base64 import b64decode
from urllib.parse import urlencode
from twilio.rest import Client
from datetime import datetime


def decrypt(cipher_text):

    """ Decrypts KMS encrypted text """
    return boto3.client('kms').decrypt(CiphertextBlob=b64decode(cipher_text))[
        u'Plaintext'].decode()


def fetch_lambda_invocation_timestamp():
    """ Fetch the last invocation timestamp for this lambda function """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('lambda_invocation_logs')

    try:
        response = table.get_item(
            Key={
                'aws_lambda_function_name': os.environ['AWS_LAMBDA_FUNCTION_NAME']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        return item['invocation_timestamp_utc']



def update_lambda_invocation_timestamp():
    """ Updates the timestamp for this lambda function in DynamoDB """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('lambda_invocation_logs')

    table.put_item(
        Item={
            'aws_lambda_function_name': os.environ['AWS_LAMBDA_FUNCTION_NAME'],
            'aws_lambda_function_version': os.environ['AWS_LAMBDA_FUNCTION_VERSION'],
            'invocation_timestamp_utc': datetime.utcnow().isoformat()
        }
    )


TWILIO_ACCONT = decrypt(os.environ['TWILIO_ACCOUNT'])
TWILIO_TOKEN = decrypt(os.environ['TWILIO_TOKEN'])
ALERT_PHONE = decrypt(os.environ['ALERT_PHONE'])
TWILIO_PHONE = decrypt(os.environ['TWILIO_PHONE'])


def handler(event, context):
    last_invocation_utc = fetch_lambda_invocation_timestamp()

    client = Client(
        TWILIO_ACCONT,
        TWILIO_TOKEN,
    )

    call = client.calls.create(to=ALERT_PHONE, from_=TWILIO_PHONE,
                               url='http://twimlets.com/message?{}'.format(
                                   urlencode({
                                       'Message[0]': "Baby needs to go potty",
                                   })),
                               )
    print(call.sid)

    update_lambda_invocation_timestamp()
