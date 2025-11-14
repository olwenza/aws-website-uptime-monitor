# Create a folder
mkdir lambda_dashboard
cd lambda_dashboard

# Copy your Python script
cp ../generate_dashboard.py .

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies locally
pip install pandas matplotlib boto3 -t .

# Deactivate virtualenv
deactivate

# Zip everything
zip -r ../dashboard_lambda.zip .
