import boto3
import ssb
import report
import datetime
import json

def lambda_handler(event, context):
    session = boto3.Session()

    
    sts = session.client("sts")
    arn = sts.get_caller_identity()["Arn"]
    account = sts.get_caller_identity()["Account"]
    
    # print("=" * 60)
    # print(f"ARN: {arn}")
    # print("=" * 60)

    
    results = ssb.checks(session)
    results.sort(key=lambda x: x["title"])
    
    file = report.generate_report(account, results)
    bucket = "ssb-reports-bucket"

    # with open("./report.html", 'w') as f:
    #     f.write(file)

    name = f"report_{account}_{datetime.date.today().isoformat()}.html"
    
    if upload_file(bucket, name, file):
        return {
            'statusCode': 200,
            "body": file,
            "headers": {
                'Content-Type': 'text/html',
            }
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("upload fail")
        }
    
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