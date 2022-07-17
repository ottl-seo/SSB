import boto3
from datetime import date
import json
import report
import os

sts = boto3.client("sts")
account = sts.get_caller_identity()["Account"]

resource = boto3.resource('s3')
bucket = resource.Bucket(os.environ["Bucket"][13:])
lamb = boto3.client('lambda')

def lambda_handler(event, context):

    try:
        obj = bucket.Object(f'result-{date.today().isoformat()}.json').get()
        results = json.loads(obj["Body"].read().decode('utf-8'))
        html = report.generate_report(account, results)
        
        bucket.put_object(Key=f"report-{date.today().isoformat()}.html", Body=bytes(html.encode('UTF-8')))
        
        return {
            'statusCode': 200,
            "body": html,
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        
    except Exception as e:

        lamb.invoke(FunctionName=os.environ["SSB"].split(":")[-1], InvocationType='Event')

        try:
            bucket.Object("temp").get()
            return {
                'statusCode': 200,
                "body": "레포트를 생성 중 입니다. 약 5분 후 새로고침해주세요. 이메일을 구독하셨다면, 메일로 알림을 받을 수 있습니다.",
                "headers": {
                    'Content-Type': 'text/html;charset=UTF-8',
                }
            }
        
        except:
            bucket.put_object(Key="temp", Body="")
            return {
                'statusCode': 200,
                "body": "레포트를 생성 중 입니다. 약 5분 후 새로고침해주세요. 이메일을 구독하셨다면, 메일로 알림을 받을 수 있습니다.",
                "headers": {
                    'Content-Type': 'text/html;charset=UTF-8',
                }
            }
        