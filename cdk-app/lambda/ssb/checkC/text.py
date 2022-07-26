
test6_1 = {
    # [Danger] Account의 S3 퍼블릭 엑세스 설정 확인

    "title": "[Test06-1] Account의 S3 퍼블릭 엑세스 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "Account의 S3 퍼블릭 엑세스 설정이 블록되어 있습니다.", "link": ""}
        ]
    },

    "Warning": {
        "level": "Warning",
        "msg": [
                {"text": "Account의 일부 퍼블릭 엑세스 설정이 허용되어 있습니다. 보안을 위해 가급적 차단해주세요.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}

test6_2 = {
    # [Danger] Bucket의 S3 퍼블릭 엑세스 설정 확인

    "title": "[Test06-2] Bucket의 S3 퍼블릭 엑세스 설정 여부",

    "Success": {
        "level": "Success",
        "msg": [
            {"text": "모든 버킷의 S3 퍼블릭 엑세스 설정이 블록되어 있습니다.", "link": ""}
        ]
    },

    "Danger": {
        "level": "Danger",
        "msg": [
                {"text": "일부 버킷의 퍼블릭 엑세스 설정이 허용되어 있습니다. 보안을 위해 가급적 차단해주세요.", "link":""}, 
            ]
    },
    
    "Error": {
        "level": "Error",
        "msg": [{"text":"진단 중 에러가 발생하였습니다.", "link": ""}]
    }

}
