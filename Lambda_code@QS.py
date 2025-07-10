--Lambda code to trigger the Quicksight dahboard to update based on the SQS queue
-- I didnt share my account details here. change it according to yours

import json
import boto3
import os

quicksight = boto3.client('quicksight')


def lambda_handler(event, context):
    print("Received SQS Event:", json.dumps(event, indent=2))

    aws_account_id = os.environ['AWS_ACCOUNT_ID']
    dataset_id = os.environ['DATASET_ID']

    # Generate unique ingestion ID
    ingestion_id = 'ingestion-' + context.aws_request_id[:8]

    for record in event['Records']:
        try:
            body = json.loads(record['body'])

            # S3 event structure inside SQS body
            s3_event = json.loads(body['Message']) if 'Message' in body else body
            s3_info = s3_event['Records'][0]['s3']
            bucket = s3_info['bucket']['name']
            key = s3_info['object']['key']

            print(f"New file landed: s3://{bucket}/{key}")

            # Trigger QuickSight dataset ingestion
            response = quicksight.create_ingestion(
                AwsAccountId=aws_account_id,
                DataSetId=dataset_id,
                IngestionId=ingestion_id
            )

            print("QuickSight ingestion triggered:", response)

        except quicksight.exceptions.ResourceExistsException:
            print("Ingestion already in progress.")

        except Exception as e:
            print("Error processing record:", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('QuickSight refresh triggered.')
    }

