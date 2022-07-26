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

    obj_A = bucket.Object(f'result-A-{date.today().isoformat()}.json').get()
    obj_B = bucket.Object(f'result-B-{date.today().isoformat()}.json').get()
    obj_C = bucket.Object(f'result-C-{date.today().isoformat()}.json').get()
    obj_D = bucket.Object(f'result-D-{date.today().isoformat()}.json').get()
        
    # A,B,C,D 파일 읽어오고 
    results_A = json.loads(obj_A["Body"].read().decode('utf-8'))
    results_B = json.loads(obj_B["Body"].read().decode('utf-8'))
    results_C = json.loads(obj_C["Body"].read().decode('utf-8'))
    results_D = json.loads(obj_D["Body"].read().decode('utf-8'))
    
    # Fix: array가 아니어서 생기는 오류
    result_Blist = []
    result_Blist.append(results_B)
    result_Clist = []
    result_Clist.append(results_C)
    
    ## 배열 results에 인덱스로 추가
    results = []
    allLambdaResult=[results_A, result_Blist, result_Clist, results_D];
    for eachLambdaResult in allLambdaResult:
        for r in eachLambdaResult:
            results.append(r)
    
    name = f"results.json"
    upload_file(bucket, name, json.dumps(results))
    
    return 0
    
    # 정렬
    #results.sort(key=lambda x: x[0])
    """
    html = report.generate_report(account, results)
    bucket.put_object(Key=f"report-{date.today().isoformat()}.html", Body=bytes(html.encode('UTF-8')))
    
    return {
        'statusCode': 200,
        "body": html,
        "headers": {
            'Content-Type': 'text/html',
        }
    }
    """
    
def upload_file(bucket, name, file):
    encoded = bytes(file.encode('UTF-8'))
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=name, Body=encoded)
        return True
    except:
        return False
