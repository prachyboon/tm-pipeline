import json
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel("INFO")

# TODO: these should be used SSM-Parameter Store instead or inject ENV variable from Lambda
sfn = boto3.client('stepfunctions')
PIPELINE_ARN = 'arn:aws:states:ap-southeast-1:342076896000:stateMachine:tm-etl-workflow'


def lambda_handler(event, context):
    logger.info(event)
    logger.info("file landing: {}".format(event['Records'][0]['s3']['object']['key']))

    ingested_file = event['Records'][0]['s3']['object']['key']
    ingested_table = ingested_file.split('.')[0].split('/')[-1]  # to extract table name from partition data
    ingested_id = datetime.strftime(datetime.now(), '%Y%m%dT%H%M')

    response = sfn.start_execution(
        stateMachineArn=PIPELINE_ARN,
        name='{}-{}'.format(ingested_table, ingested_id),
        input=json.dumps({"ingestedFile": ingested_file})
    )
    logger.info("start ingestion response: {}".format(response))
    return {
        'statusCode': 200,
        'body': json.dumps({"statusCode": 200})
    }
