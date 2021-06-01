import json
import boto3
from boto3.session import Session

def lambda_handler(event, context):

    try:
        # QUERY_STRING から path パラメータを取得
        key = event.get('queryStringParameters').get('path')

        session = Session()

        # パラメータストアから値を取得
        ssm_client = boto3.client('ssm')
        ssm_response = ssm_client.get_parameter(
            Name = 'S3DownloadFileSuffix',
            WithDecryption = False
        )

        # バケット名を取得
        S3DownloadFileSuffix = ssm_response['Parameter']['Value']
        BUCKET = 's3-download-file-bucket-' + S3DownloadFileSuffix

        # バケットを取得
        s3_client = session.client('s3')

        # 有効期間： 30 秒の presigned URL を発行
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod = 'get_object',
            Params = {'Bucket' : BUCKET, 'Key' : key},
            ExpiresIn = 30,
            HttpMethod = 'GET')

    except Exception as e:
        print(e)
        raise e

    return {
        "statusCode": 301,
        "headers": {
            "Location": "{}".format(presigned_url)
        },
        "body": json.dumps({
            "key": key
        }),
    }
