import boto3
from datetime import date, datetime, timedelta, timezone
import os

def lambda_handler(event, context):

    s3 = boto3.client('s3', config=boto3.session.Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
    sns= boto3.client("sns")
    bucket_name = os.environ["Bucket"][13:]
    object_name = f'result-{date.today().isoformat()}.html'

    topic = os.environ["Topic"]

    try:
        response = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,
                                                        'Key': object_name},
                                                ExpiresIn=3600)        
        
        KST = timezone(timedelta(hours=9))
        expired = datetime.now(tz=KST) + timedelta(hours=1)

        sns.publish(TopicArn=topic, Message=f"""        
        리포트 파일의 미리 서명된(pre-signed) url을 생성하였습니다.
        {expired.isoformat()} 까지 접속 가능합니다.

        {response}
        """)


        return {
            'statusCode': 200,
            "body": "Success",
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        
    except Exception as e:

        sns.publish(TopicArn=topic, Message=f"""        
        리포트를 불러오는 중 오류가 발생하였습니다.

        {e}
        """)

        return {
            'statusCode': 400,
            "body": "Failed",
            "headers": {
                'Content-Type': 'text/html',
            }
        }