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


def check05(session):

    s = time.time()

    title = "05 Turn CloudTrail On"
    cloudtrail = session.client('cloudtrail')

    ret = {
        "title": title,
        "alerts":[],
        "tables": [
            {
                "cols": ["Trail", "multi region", "logging"],
                "rows": []
            }
        ]
    }

    code = "Success"
    code_multi_region = "Success"
    logging = 0
    multi_region = 0
    errorMsg = ""

    try:

        trails = cloudtrail.describe_trails()["trailList"]

        if len(trails) == 0:
            # utils.print_fail("No trails exists")
            code = "NO_TRAIL"
            code_multi_region = "NO_TRAIL"

        for trail in trails:
            # print(trail["TrailARN"])
            if(trail["IsMultiRegionTrail"]):
                # utils.print_pass("Multi region trail: True")
                multi_region += 1
            else:
                # utils.print_fail("Multi region trail: False")
                code_multi_region = "Warning"

            status = cloudtrail.get_trail_status(Name=trail["TrailARN"])
            if(status["IsLogging"]):
                # utils.print_pass("logging: True")
                logging += 1

            else:
                # utils.print_fail("logging: False")
                # append_alert(ret, "Danger", [[f"{trail['TrailARN']}가 logging되고 있지 않습니다.", ""]])
                code = "Warning"

            append_table(ret, 0, [trail["TrailARN"], trail["IsMultiRegionTrail"], status["IsLogging"]])
        
        if code != "NO_TRAIL" and logging == 0:
            code = "ALL_OFF"

        if code != "NO_TRAIL" and multi_region == 0:
            code_multi_region = "NO_MULTI"

    except botocore.exceptions.ClientError as error:
        errorMsg = error.response["Error"]["Message"]
        code = "Error"



    ret["alerts"].append({
        "level": text.test5_1[code]["level"],
        "msg": text.test5_1[code]["msg"] + [{"text":errorMsg, "link":""}],
        "title": text.test5_1["title"]
    })

    if code != "Error":
        ret["alerts"].append({
            "level": text.test5_2[code_multi_region]["level"],
            "msg": text.test5_2[code_multi_region]["msg"] + [{"text":errorMsg, "link":""}],
            "title": text.test5_2["title"]
        })

    print(title, time.time() - s)

    return ret
    
if __name__ == "__main__":
    import boto3
    session = boto3.Session()

    print(check07(session))
