import json
import boto3
import urllib.parse

s3 = boto3.client("s3")
textract = boto3.client("textract")

def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"])

    print(f"Processing {key}")

    response = textract.analyze_expense(
        Document={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            } }   )

    output_key = key.replace("raw/", "json/") + ".json"

    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=json.dumps(response, indent=2),
        ContentType="application/json"
    )

    print("Saved output:", output_key)

    return {"status": "success"}
