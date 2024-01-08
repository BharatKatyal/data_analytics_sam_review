import boto3
from datetime import datetime
import random
import time
import json
import calendar  # Add this line to import the calendar module
import os




# The kinesis stream defined in AWS console
stream_name = os.environ['KinesisStreamName']

k_client = boto3.client('kinesis', region_name='us-east-1')

def lambda_handler(event, context):
    for _ in range(10):
        order_id = random.randint(1000, 9999)
        customer_id = random.randint(100, 999)
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 10)
        price = round(random.uniform(10, 500), 2)
        order_timestamp = calendar.timegm(datetime.utcnow().timetuple())

        order_data = {
            'order_id': order_id,
            'customer_id': customer_id,
            'product_id': product_id,
            'quantity': quantity,
            'price': price,
            'order_timestamp': order_timestamp
        }

        put_to_stream(order_data, order_id)

        time.sleep(1)

def put_to_stream(order_data, order_id):
    payload = json.dumps(order_data)
    print(payload)

    k_client.put_record(
        StreamName=stream_name,
        Data=payload,
        PartitionKey=str(order_id))
