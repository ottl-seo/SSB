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



if __name__ == "__main__":
    import boto3
    session = boto3.Session()

    print(check04(session))
