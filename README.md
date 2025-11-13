# Project Title

AWS - Website uptime monitor

## Description
Project check website health (check website every 5 minutes) sends notification upon encountering issues.


# Outline 
1. Check if website is loading
2. Check how fast website loads
3. Check if website is showing the right content
4. If any of the above checks fails, send SNS notification
5. Store all test results in DynamoDB
6. Create S3 Dashboard showing % time up this month, Average response time & number of incidents this month

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

* Zip website-uptime-monitor-lamda.py to zip file to be used in aws lambda
```
zip function.zip website-uptime-monitor-lamda.py
```

* Create the lamda function in aws lambda (get role = arn of iam user executing function)
```
aws lambda create-function \
  --function-name websiteUptimeMonitor \
  --runtime python3.12 \
  --role arn:aws:iam::697227439720:role/lambda-cost-comparison-role \
  --handler website-uptime-monitor-lamda.lambda_handler \
  --zip-file fileb://function.zip
```

* Test the lamda functioon - print output to response.json file
```
aws lambda invoke \
  --function-name websiteUptimeMonitor \
  --payload '{}' \
  response.json

cat response.json
```

### 2- Check how fast website loads
* Run script to upload to S3 (Execute previous step first)
**- TBD**
```
TBD
``` 

### 3- Check if website is showing the right content
**- TBD**
```
TBD
``` 

### 4- If any of the above checks fails, send SNS notification
**- TBD**
```
TBD
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