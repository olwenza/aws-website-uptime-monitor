import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime, timezone

# ---------- CONFIG ----------
DDB_TABLE = "WebsiteMonitor"
S3_BUCKET = "website-monitor-ivan"
MONTH_PREFIX = datetime.utcnow().strftime("%Y/%m/")  # e.g., 2025/11/
DASHBOARD_KEY = f"{MONTH_PREFIX}website-monitor-dashboard.png"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DDB_TABLE)
s3 = boto3.client("s3")


def generator_handler(event, context):
    # ---------- GET DATA ----------
    start_of_month = datetime(datetime.utcnow().year, datetime.utcnow().month, 1, tzinfo=timezone.utc)
    start_iso = start_of_month.isoformat()

    response = table.scan(
        FilterExpression="timestamp >= :start",
        ExpressionAttributeValues={":start": start_iso}
    )
    items = response.get('Items', [])

    # Pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression="timestamp >= :start",
            ExpressionAttributeValues={":start": start_iso},
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))

    if not items:
        raise Exception("No monitoring data found for this month.")

    # ---------- CONVERT TO DF ----------
    df = pd.DataFrame(items)
    df['load_time_ms'] = df['load_time_ms'].astype(float)
    df['isPass'] = df['isPass'].astype(bool)
    df['status'] = df['status'].astype(str)

    # ---------- METRICS ----------
    uptime_percentage = (df['status'] == 'UP').mean() * 100
    average_response_time = df['load_time_ms'].mean()
    number_of_incidents = ((df['status'] != 'UP') | (~df['isPass'])).sum()

    # ---------- DASHBOARD ----------
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))

    ax[0].bar(['Uptime %'], [uptime_percentage], color='green')
    ax[0].set_ylim(0, 100)
    ax[0].set_ylabel('%')
    ax[0].set_title('Uptime %')

    ax[1].bar(['Avg Response Time'], [average_response_time], color='blue')
    ax[1].set_ylabel('ms')
    ax[1].set_title('Average Response Time')

    ax[2].bar(['Incidents'], [number_of_incidents], color='red')
    ax[2].set_ylabel('Count')
    ax[2].set_title('Incidents this Month')

    plt.tight_layout()

    # ---------- SAVE TO S3 ----------
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    s3.put_object(Bucket=S3_BUCKET, Key=DASHBOARD_KEY, Body=buf, ContentType='image/png')

    return {
        "status": "success",
        "s3_key": DASHBOARD_KEY
    }
