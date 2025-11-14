import json
import urllib3
import time
import boto3
import time
import uuid
from datetime import datetime, timezone

### code for lambda function request
# {
#     "url": "https://www.abeventcenter.com",
#     "expected_text": "San Diegos most affordable event space!"
# }

#Custom libs
import util

HTTP = urllib3.PoolManager()
SNS_CLIENT = boto3.client('sns')
TABLE_NAME = "WebsiteMonitor"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:697227439720:topic-website-uptime-monitor"

def lambda_handler(event, context):

    # PREVENT unbound variable crashes
    body = None
    status_code = None
    load_time_ms = None
    content_match = None
    status = "DOWN"
    isPass = True
    error = None

    # Get parameters from the event
    url = event.get("url", "https://example.com")
    expected_text = event.get("expected_text", None)
    message = f"Uptime monitor test failed for your website {url}" 

    try:
        start_time = time.time()
        response = HTTP.request("GET", url, timeout=10.0)
        end_time = time.time()

        # Calculate response time in milliseconds
        load_time_ms = round((end_time - start_time) * 1000, 2)
        status_code = response.status
        
        body = response.data.decode("utf-8", errors="ignore")

        if 200 <= int(status_code) < 400:
            status = "UP"

        if expected_text:
            if expected_text in body:
                content_match = True
            else:
                content_match = False
                isPass = False
                error = "Content didn't match!"
        else:
            isPass = False 
            error = "Expected text is null!"
            
    except Exception as e:
        isPass = False
        error = str(e) 

    finally: 
        result = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "url": url,
            "status": status,
            "status_code": status_code,
            "load_time_ms" : load_time_ms,
            "content_match": content_match,
            "expected_text": expected_text,
            "error" : error,
            "isPass" : isPass
        }

        # If test fails for any other reason
        if not isPass:
            util.sendSNS(SNS_CLIENT, SNS_TOPIC_ARN, message)    # Send SNS email 

        #Insert test result to table
        util.insertRowToDynamoDB(result, TABLE_NAME)

    # Return JSON response
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }