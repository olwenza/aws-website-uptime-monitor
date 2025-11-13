# Project Title

AWS - Website uptime monitor

## Description
Project check website health (check website every 5 minutes) and sends notification upon encountering issues.


# Outline 
1. Check if website is loading
2. Check how fast website loads
3. Check if website is showing the right content
4. If any of the above checks fail, send SNS notification
5. Store all test results in DynamoDB
6. Create S3 Dashboard showing time up percentage this month, Average response time & number of incidents this month

## Getting Started

### Dependencies
 
* Install Homebrew if not already installed
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
 
 * Update Homebrew
 ```
 brew update
 ```

* Install AWS CLI
```
brew install awscli
```

* Verify installation.
```
awscli --version
```
 
* Configure awscli with account credentials
```
awscli configure
```

### Installing

* TBD/NA

### Executing program
### 1- Check if website is loading
* Create trust policy file to run lambda function
```
aws iam create-role \
  --role-name lambda-website-uptime-monitor-role \
  --assume-role-policy-document file://json/trust-policy.json
```
* Attach policy (above) for basic lamda execution to write to Cloudwatch logs
```
aws iam attach-role-policy \
  --role-name lambda-website-uptime-monitor-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

* Create a python file for the lambda function code
```
touch website-uptime-monitor-lamda.py
```

* Zip the file website-uptime-monitor-lamda.py to a zip file to be used in aws lambda
```
zip function.zip website-uptime-monitor-lamda.py
```

* Create the lamda function in aws lambda (--role = arn of iam user executing the function)
```
aws lambda create-function \
  --function-name websiteUptimeMonitor \
  --runtime python3.12 \
  --role arn:aws:iam::697227439720:role/lambda-website-uptime-monitor-role \
  --handler website-uptime-monitor-lamda.lambda_handler \
  --zip-file fileb://function.zip
```

* Run the lamda functioon and print output to response.json file
```
aws lambda invoke \
  --function-name websiteUptimeMonitor \
  --payload '{}' \
  response.json

cat response.json
```

### 2- Check how fast website loads
* Code updated to compute response time and return response time

### 3- Check if website is showing the right content
* Code updated to check if site showing correct content.
* Call lamda fuction with the following content to test a running site
```
{
    "url": "https://www.abeventcenter.com",
    "expected_text": "San Diegos most affordable event space!"
}
``` 
* Call lamda fuction with the following content to test wrong content
```
{
    "url": "https://www.abeventcenter.com",
    "expected_text": "WRONG CONTENT!"
}
``` 

* Call lamda fuction with the following content for a non running site
```
{
    "url": "https://www.sdwebtech.com",
    "expected_text": "San Diegos most affordable event space!"
}
```

### 4- If any of the above checks fails, send SNS notification

* Create SNS topic
```
aws sns create-topic --name topic-website-uptime-monitor
```

* Subscribe to topic from previous step (use arn returned from previous command)
```
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:697227439720:topic-website-uptime-monitor \
  --protocol email \
  --notification-endpoint olwenza@yahoo.com
``` 

* Allow Lambda’s IAM role to publish to that specific SNS topic
```
aws iam put-role-policy \
    --role-name lambda-cost-comparison-role \
    --policy-name AllowSNSTopicPublish \
    --policy-document file://json/sns-publish-policy.json
```

### 5- Store all test results in DynamoDB
**- TBD**
```
TBD
``` 

### 6- Create S3 Dashboard showing % time up this month, Average response time & number of incidents this month
**- TBD**
```
TBD
```

## Authors

Contributors names and contact info

Ivan Augustino
[@ivanaugustino](https://www.linkedin.com/in/ivanaugustino/)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [General Public License (GPL) - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)