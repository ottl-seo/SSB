import botocore.exceptions
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

import sys, os
sys.path.append(os.path.dirname(__file__))
import text

def append_alert(ret, alert, title):
    ret["alerts"].append({
        "level": alert["level"],
        "msg": alert["msg"],
        "title": title
    })

def append_table(ret, num, row):
    ret["tables"][num]["rows"].append(row)

############## CHECK C ###############

def check06(session):

    s = time.time()
    title = "06 Prevent Public Access to Private S3 Buckets"

    s3 = session.client('s3')
    s3control = session.client('s3control')
    sts = session.client('sts')

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["이름", "퍼블릭 엑세스"],
                "rows": []
            }
        ]
    }
    code = "Success"
    errorMsg = ""

    try:
        account_id = sts.get_caller_identity()["Account"]
        account_policy = s3control.get_public_access_block(AccountId=account_id)["PublicAccessBlockConfiguration"]

        for key, val in account_policy.items():
            if val:
                pass
            else:
                code = "Warning"

        append_table(ret, 0, ["Account 설정", "일부 허용" if code == "Warning" else "차단"])

        ret["alerts"].append({
            "title": text.test6_1["title"],
            "level": text.test6_1[code]["level"],
            "msg": text.test6_1[code]["msg"]
        })

        code_bucket = "Success"
        errorMsg_bucket = ""
        buckets = s3.list_buckets()["Buckets"]


        _executor = ThreadPoolExecutor(20)

        async def run(bucket):
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(_executor, lambda: get_pab(bucket))
            return response

        async def execute():
            task_list = [asyncio.ensure_future(run(bucket["Name"])) for bucket in buckets]
            done, _ = await asyncio.wait(task_list)
            results = [d.result() for d in done]
            return results

        def get_pab(bucket):
            try:
                status = s3.get_public_access_block(Bucket=bucket)
                for _, val in status["PublicAccessBlockConfiguration"].items():
                    if val == False:
                        return bucket, False
                return bucket, True
            except:
                return bucket, True

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(execute())
        loop.close()

        for bucket, status in results:
            if status == False:
                code_bucket = "Danger"
            append_table(ret, 0, [bucket, "차단" if status else "일부 허용"])                

        if code == "Warning":
            ret["alerts"].append({
                "level":text.test6_2[code_bucket]["level"],
                "msg": text.test6_2[code_bucket]["msg"] + [{"text":errorMsg_bucket, "link":""}],
                "title": text.test6_2['title']
            })

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
            ret["alerts"].append({
                "title": text.test6_1["title"],
                "level": text.test6_1["Success"]["level"],
                "msg": text.test6_1["Success"]["msg"]
            })
        else:
            code = "Error"
            ret["alerts"].append({
                "title": text.test6_1["title"],
                "level": text.test6_1[code]["level"],
                "msg": text.test6_1[code]["msg"] + [{"text":error.response["Error"]["Message"], "link":""}]
            })

    print(title, time.time() - s)
    return ret


if __name__ == "__main__":
    import boto3
    session = boto3.Session()

    print(check06(session))
