# A basic utility/helper class
import json
 
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