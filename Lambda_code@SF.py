--Lambda code to trigger the Step function which further triggers athena and stores the transformed data into s3

import json
import boto3
import os

s3 = boto3.client('s3')
stepfunctions = boto3.client('stepfunctions')

# Constants
BUCKET_NAME = 'assurebuckets32pkkuppili'
PREFIX = 'input/'
STATE_MACHINE_ARN = 'arn:aws:states:us-east-2:178795994454:stateMachine:athenastatefunctest'

# Query to execute
QUERY_STRING = """
CREATE TABLE samples3db.curated_sales_data_parquet
WITH (
  format = 'PARQUET',
  parquet_compression = 'SNAPPY',
  external_location = 's3://assurebuckets32pkkuppili/athena_output/curated_sales_data_parquet/'
) AS
select f.payment_key,f.coustomer_key,f.store_key,f.item_key,f.quantity,f.unit,f.unit_price,f.total_price,
c.name,c.contact_no,i.item_name,i.desc ,i.supplier,s.division,s.district,t.trans_type,t.bank_name
from samples3db.fact_table f
left join samples3db.customer_table c on f.coustomer_key = c.coustomer_key
left join samples3db.item_table i on f.item_key = i.item_key
left join samples3db.store_table s on f.store_key = s.store_key
left join samples3db.payment_table t on f.payment_key = t.payment_key
"""


def lambda_handler(event, context):
    # List current files in the prefix
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
        objects = response.get('Contents', [])
        # Filter only actual files (ignore folders)
        files = [obj for obj in objects if not obj['Key'].endswith('/')]

        if len(files) >= 5:
            print(f"Found {len(files)} files, triggering Step Function.")

            input_payload = {
                "Query": QUERY_STRING
            }

            stepfunctions.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps(input_payload)
            )
            return {
                'statusCode': 200,
                'body': f"Step Function triggered with {len(files)} files."
            }
        else:
            print(f"Only {len(files)} files found. Waiting for more.")
            return {
                'statusCode': 200,
                'body': f"Only {len(files)} files found. Not triggering Step Function."
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
