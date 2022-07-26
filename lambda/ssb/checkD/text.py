

test7 = {
    # [Warning] 비용 알람 및 루트 계정 엑세스 알람

    "title": "[Test07] 비용 알람 및 루트 계정 엑세스 알람 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "알람이 켜져있습니다. 비용 및 루트 계정 알람인지 확인해 주세요.", "link": ""}
        ]
    },

    "NO_ALARM": {
        "level": "Warning",
        "msg": [
                {"text": "알람이 설정되어있지 않습니다. 보안을 위해 알람을 설정해주세요.", "link":""}, 
            ]
    },
    
    "Info": {
        "level": "Info",
        "msg": [
                {"text": "워크샵", "link": "https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms"},
                {"text": "을 통하여 비용 및 루트 계정 알람을 설정할 수 있습니다.", "link": ""}
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }
}

test8 = {
    # [Warning] VPC, Subnet, Security Group

    "title": "[Test08] VPC, Subnet, Security Group 사용",

    "Warning": {
        "level": "Warning",
        "msg": [
            {"text": "EC2 Global View 서비스", "link": "https://us-east-1.console.aws.amazon.com/ec2globalview/home"},
            {"text": "를 통해 전체 리전별 VPC/Subnet/SG/ EC2 현황을 확인할 수 있으며 사용하지 않는 리소스 등이 있다면 검토 후 삭제하는 것을 권유드립니다.", "link": ""}
        ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }
}

test9 = {
    # [Warning] Trusted Advisor 설정 여부

    "title": "[Test09] Trusted Advisor 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "Trusted Advisor가 작동 중 입니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
                {"text": "Trusted Advisor가 꺼져있습니다.", "link":""}, 
            ]
    },

    "Subscribe": {
        "level": "Warning",
        "msg": [
                {"text": " Business Support 이상의 Support Plan 을 이용하시면 Trusted Advisor 에서 더 다양한 지표들에 대해 점검하고 조치 가이드를 받으실 수 있습니다.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test10 = {
    # [Warning] GuardDuty 설정 여부

    "title": "[Test10] GuardDuty 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "GuardDuty가 작동 중 입니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
                {"text": "GuardDuty가 꺼져있습니다.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}