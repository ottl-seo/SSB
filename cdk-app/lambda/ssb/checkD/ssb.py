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

############## CHECK D ###############
def check07(session):

    s = time.time()

    title = "07 Configure Alarms"
    alarms_tot = []
    
    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["리전", "이름"],
                "rows": []
            }
        ]
    }

    regions = sorted(list(map(lambda x: x["RegionName"], session.client("ec2").describe_regions()["Regions"])))
    _executor = ThreadPoolExecutor(20)

    async def run(region):
        loop = asyncio.get_running_loop()
        cloudwatch = session.client("cloudwatch", region_name=region)
        response = await loop.run_in_executor(_executor, cloudwatch.describe_alarms)
        return response

    async def execute():
        task_list = [asyncio.ensure_future(run(region)) for region in regions]
        done, _ = await asyncio.wait(task_list)

        results = [d.result() for d in done]
        return results

    code = "Success"
    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(execute())
        loop.close()

        for result in results:
            for alarm in result["MetricAlarms"]:
                arn = alarm["AlarmArn"].split(":")
                region = arn[3]
                name = arn[6]
                alarms_tot.append((region, name))
            

        for alarm in alarms_tot:
            append_table(ret, 0, [alarm[0], alarm[1]])


        if len(alarms_tot) == 0:
            code = "NO_ALARM"
        else:
            code = "Success"

    except botocore.exceptions.ClientError as error:
        code = "Error"
        errorMsg = error.response["Error"]["Message"]

    ret["alerts"].append({
        "level": text.test7[code]["level"],
        "msg": text.test7[code]["msg"],
        "title": text.test7["title"]
    })
    
    ret["alerts"].append({
        "level": text.test7["Info"]["level"],
        "msg": text.test7["Info"]["msg"],
        "title": text.test7["title"]
    })


    print(title, time.time() - s)

    return ret
    

def check08(session):

    s = time.time()
    title = "08 Delete unused VPCs, Subnets & Security Groups"

    ret = {
        "title": title,
        "alerts":[],
        "tables": []
    }
    
    ret["alerts"].append({
        "level": text.test8["Warning"]["level"],
        "msg": text.test8["Warning"]["msg"],
        "title": text.test8["title"]
    })

    print(title, time.time() - s)

    return ret


def check09(session):
    s = time.time()
    title = "09 Enable AWS Trusted Advisor"

    support = session.client('support', region_name='us-east-1')
    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["Trusted Advisor 상태"],
                "rows": []
            }
        ]
    }
    code = "Warning"
    errorMsg = ""

    try:
        support.describe_trusted_advisor_checks(language="en")
        # utils.print_pass("Trusted Advisor is enabled")
        code = "Success"
        append_table(ret, 0, ["켜져 있음"])

    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "SubscriptionRequiredException":
            append_table(ret, 0, [text.test9["Subscribe"]["msg"][0]["text"]])
            code = "Subscribe"
            
        else:
            errorMsg = error.response["Error"]["Message"]
            code = "Error"

    ret["alerts"].append({
        "title": text.test9["title"],
        "level": text.test9[code]["level"],
        "msg": text.test9[code]["msg"] + [{"text":errorMsg, "link":""}]
    })
    print(title, time.time() - s)

    return ret

def check10(session):
    s = time.time()
    title = "10 Enable GuardDuty"
    guardDuty = session.client("guardduty", region_name='ap-northeast-2')
    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": [],
                "rows": []
            }
        ]
    }
    code = "Success"
    errorMsg = ""

    try:
        detectors = guardDuty.list_detectors()["DetectorIds"]
        if len(detectors) == 0:
            # utils.print_fail("GuardDuty is disabled")
            code = "Warning"

        for detector in detectors:
            detector = guardDuty.get_detector(DetectorId=detector)
            status = detector["Status"] 
            if status == "ENABLED":
                # utils.print_pass("GuardDuty is enabled")
                # append_alert(ret, "Success", [["GuardDuty가 활성화되어 있습니다.", ""]])
                pass

            else:
                # utils.print_fail("GuardDuty is disabled")
                code = "Warning"


    except botocore.exceptions.ClientError as error:
        errorMsg = error.response["Error"]["Message"]
        code = "Error"

    ret["alerts"].append({
        "title": text.test10["title"],
        "level": text.test10[code]["level"],
        "msg": text.test10[code]["msg"] + [{"text":errorMsg, "link":""}]
    })

    print(title, time.time() - s)

    return ret




async def generate_async_check(check, session, _executor):

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(_executor, check, session)
    return response
    


async def async_checks(session, _executor, tests):

    checks = [check09, check10]

    task_list = [asyncio.ensure_future(generate_async_check(checks[i-1], session, _executor)) for i in tests]
    

    done, _ = await asyncio.wait(task_list)
    results = [d.result() for d in done]

    return results

def checks(session, tests=[1,2]):

    _executor = ThreadPoolExecutor(5)

    try:
        iam = session.client('iam')
        iam.generate_credential_report()
    except:
        pass

    s = time.time()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_checks(session, _executor, tests))
    print(time.time() - s)

    return result
    
if __name__ == "__main__":
    import boto3
    session = boto3.Session()

    print(check10(session))
