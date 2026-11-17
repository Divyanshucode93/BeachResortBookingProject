import json
import os
import boto3
from botocore.exceptions import ClientError

DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'ResortBookings')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    # Handle CORS preflight request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': ''
        }

    try:
        # Parse incoming body
        body = json.loads(event.get('body', '{}'))
        required_fields = ['bookingId', 'roomType', 'guestName', 'email', 'checkIn', 'checkOut']
        
        for field in required_fields:
            if not body.get(field):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': True
                    },
                    'body': json.dumps({"error": f"Missing required field: {field}"})
                }

        # Save to DynamoDB
        table.put_item(Item=body)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps({"message": "Booking successfully created", "bookingId": body['bookingId']})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps({"error": str(e)})
        }