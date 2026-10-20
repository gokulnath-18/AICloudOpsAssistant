
import boto3

client = boto3.client("logs", region_name="ap-south-1")

log_group = "/aws/lambda/image-processing-function"
log_stream = "2026/09/08/[$LATEST]fc6e403060a94212b254d9d7f2ae0906"

response = client.get_log_events(
    logGroupName=log_group,
    logStreamName=log_stream,
    startFromHead=True,
    limit=50
)

events = response.get("events", [])

if not events:
    print("No events found in this log stream.")
else:
    print("===== REAL AWS LAMBDA LOGS =====")

    for event in events:
        print(event["message"])
