import json
import urllib3
import time

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # Get the website URL from the event or default to example.com
    url = event.get("url", "https://www.abeventcenter.com")  # Website Up
    # url = event.get("url", "https://www.nilecomputing.com") # Website Down   
    
    try:
        start_time = time.time()
        response = http.request("GET", url, timeout=10.0)
        end_time = time.time()

        # Calculate response time in milliseconds
        load_time_ms = round((end_time - start_time) * 1000, 2)
        status_code = response.status
        
        if 200 <= status_code < 400:
            status = "UP"
        else:
            status = "DOWN"
            
        result = {
            "url": url,
            "status": status,
            "status_code": status_code,
            "load_time" : load_time_ms
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
