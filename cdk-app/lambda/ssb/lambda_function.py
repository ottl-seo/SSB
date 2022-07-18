import boto3
import ssb
import datetime
import json
import os

def lambda_handler(event, context):
    session = boto3.Session()
    sns = session.client("sns")

    try:
        results = ssb.checks(session)
        results.sort(key=lambda x: x["title"])
        
        bucket = os.environ['Bucket'][13:]
        topic = os.environ["Topic"]
        
        name = f"result-{datetime.date.today().isoformat()}.json"


        if upload_file(bucket, name, json.dumps(results)):
            sns.publish(TopicArn=topic, Message="리포트가 생성되었습니다.")
            return {
            'statusCode': 200,
            "body": json.dumps("upload success"),
            }
        else:
            sns.publish(TopicArn=topic, Message="리포트 생성 중 오류가 발생하였습니다.")
            return {
            'statusCode': 400,
            'body': json.dumps("upload fail")
            }
    except:
        sns.publish(TopicArn=topic, Message="리포트 생성 중 오류가 발생하였습니다.")



    
def upload_file(bucket, name, file):
    encoded = bytes(file.encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=name, Body=encoded)
        return True
    except:
        return False

if __name__ == "__main__":
    lambda_handler(None, None)