import json
import urllib3
import time

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # Get parameters from the event
    url = event.get("url", "https://example.com")
    expected_text = event.get("expected_text", None)

    ### code for lambda function request
    # {
    #     "url": "https://www.abeventcenter.com",
    #     "expected_text": "San Diegos most affordable event space!"
    # }

    try:
        start_time = time.time()
        response = http.request("GET", url, timeout=10.0)
        end_time = time.time()

        # Calculate response time in milliseconds
        load_time_ms = round((end_time - start_time) * 1000, 2)
        status_code = response.status
        
        body = response.data.decode("utf-8", errors="ignore")

        if 200 <= status_code < 400:
            status = "UP"
        else:
            status = "DOWN"

        # Check for expected content if provided
        content_match = None

        if expected_text:
            content_match = expected_text in body
            
        result = {
            "url": url,
            "status": status,
            "status_code": status_code,
            "load_time" : load_time_ms,
            "content_match": content_match,
            "expected_text": expected_text if expected_text else None
        }
        
    except Exception as e:
        result = {
            "url": url,
            "status": "DOWN",
            "error": str(e)
        }
    
    # Return JSON response
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }