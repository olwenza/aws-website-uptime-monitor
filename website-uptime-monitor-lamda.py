import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    # Get the website URL from the event or default to example.com
    url = event.get("url", "https://www.abeventcenter.com")  # Website Up
    # url = event.get("url", "https://www.nilecomputing.com") # Website Down   
    
    try:
        response = http.request("GET", url, timeout=5.0)
        status_code = response.status
        
        if 200 <= status_code < 400:
            status = "UP"
        else:
            status = "DOWN"
            
        result = {
            "url": url,
            "status": status,
            "status_code": status_code
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
