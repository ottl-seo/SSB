import boto3
from datetime import date
import os

def lambda_handler(event, context):

    resource = boto3.resource('s3')
    bucket_name = os.environ["Bucket"][13:]
    bucket = resource.Bucket(bucket_name)
    lamb = boto3.client('lambda')

    sns = boto3.client("sns")
    topic = os.environ["Topic"]
    
    subscriptions = sns.list_subscriptions_by_topic(TopicArn = topic)["Subscriptions"]

    for sub in subscriptions:
        if sub["SubscriptionArn"] != "PendingConfirmation":
            break
    else:
        return {
            'statusCode': 400,
            "body": "이메일로 발송된 topic을 먼저 subscribe 해주세요.",
            "headers": {
                'Content-Type': 'text/html;charset=UTF-8',
            }
        }

    endpoints = list(map(lambda x: x["Endpoint"], subscriptions))

    try:
        bucket.Object(f'result-{date.today().isoformat()}.html').get()    
        
        report_func = os.environ["Report"].split(":")[-1]
        lamb.invoke(FunctionName=report_func, InvocationType='Event')

    except:
        # report does not exist
        ssb_func = os.environ["SSB"].split(":")[-1]
        lamb.invoke(FunctionName=ssb_func, InvocationType='Event')

        
    return {
        'statusCode': 200,
        "body": f"""레포트를 생성 중 입니다. 생성 후, 이메일을 통하여 리포트 URL이 발송됩니다.
        {endpoints}
        """,
        "headers": {
            'Content-Type': 'text/html;charset=UTF-8',
        }
    }