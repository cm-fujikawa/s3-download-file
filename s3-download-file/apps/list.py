import json
import boto3
from boto3.session import Session

S3DownloadFileApi = 'XXXXXXXXXX'
REGION = 'ap-northeast-1'

def lambda_handler(event, context):

    try:
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
        DOWNLOAD_URL = 'https://{}.execute-api.{}.amazonaws.com/Prod/download?path='.format(S3DownloadFileApi, REGION)

        # バケットを取得
        s3_client = session.resource('s3')
        bucket = s3_client.Bucket(BUCKET)

        # バケット内のオブジェクトを取得
        objs = bucket.objects.filter()
        urls = [obj.key for obj in objs]

    except Exception as e:
        print(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "download_url": DOWNLOAD_URL,
            "urls": urls,
        }),
    }
