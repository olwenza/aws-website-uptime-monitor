# A basic utility/helper class
import json
import boto3
from decimal import Decimal

def sendSNS(sns_client, sns_topic_arn, message): 

    try:
        # Publish the message to the SNS topic
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message
        )
        print(f"SNS message published successfully: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('SNS message sent!')
        }
    except Exception as e:
        print(f"Error publishing SNS message: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending SNS message: {str(e)}')
        }
    
def insertRowToDynamoDB(result, tableName):
    # Initialize the Sdynamodb database
    dynamodb = boto3.client("dynamodb") 

    dynamodb.put_item(
        TableName=tableName,
        Item={
            "id": {"S": result["id"]},
            "timestamp": {"S": result["timestamp"]},
            "url": {"S": result["url"]},
            "status": {"S": result["status"]},
            "status_code": {"N": str(result.get("status_code") or 0)},
            "load_time_ms": {"N": str(Decimal(str(result.get("load_time_ms") or 0)))},
            "expected_text": {"S": result.get("expected_text", "")},
            "error": {"S": str(result.get("error", ""))},
            "content_match": {"BOOL": bool(result.get("content_match", False))}
        }
    )     