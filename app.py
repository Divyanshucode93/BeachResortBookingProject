import os
import json
from flask import Flask, send_from_directory, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__, static_url_path='', static_folder='.')

# DynamoDB configuration (uses IAM role automatically on AWS)
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'ResortBookings')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

def get_or_create_table():
    existing_tables = [t.name for t in dynamodb.tables.all()]
    if DYNAMODB_TABLE not in existing_tables:
        print(f"Creating DynamoDB table {DYNAMODB_TABLE}...")
        new_table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE,
            KeySchema=[{'AttributeName': 'bookingId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'bookingId', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        new_table.wait_until_exists()
        return new_table
    return dynamodb.Table(DYNAMODB_TABLE)

# Initialize DynamoDB resource (relies on EC2 Instance Profile credentials)
try:
    table = get_or_create_table()
except Exception as e:
    print(f"Warning: DynamoDB initialization issue: {e}")
    table = dynamodb.Table(DYNAMODB_TABLE)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/bookings', methods=['POST', 'OPTIONS'])
def handle_bookings():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        body = request.get_json()
        required_fields = ['bookingId', 'roomType', 'guestName', 'email', 'checkIn', 'checkOut']
        for field in required_fields:
            if not body or not body.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        if table:
            table.put_item(Item=body)
        else:
            return jsonify({"error": "Database table not initialized"}), 500

        return jsonify({"message": "Booking successfully created", "bookingId": body['bookingId']}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)