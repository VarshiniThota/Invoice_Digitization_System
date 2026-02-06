import boto3
from botocore.exceptions import ClientError
import os

REGION = "ap-south-1"
BUCKET_NAME = "invoice-bucket-var1307"   


def create_bucket_if_not_exists():
    s3 = boto3.client("s3", region_name=REGION)

    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint": REGION
            }
        )
        print(f" Bucket created: {BUCKET_NAME}")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "BucketAlreadyOwnedByYou":
            print("Bucket already exists, continuing...")
        else:
            raise e


def upload_file_to_s3(file_path):
    s3 = boto3.client("s3", region_name=REGION)

    file_name = os.path.basename(file_path)
    s3_key = f"raw/{file_name}"

    s3.upload_file(file_path, BUCKET_NAME, s3_key)
    print(f"File uploaded to s3://{BUCKET_NAME}/{s3_key}")


if __name__ == "__main__":
    create_bucket_if_not_exists()

    file_to_upload = input("Enter invoice file name: ")
    upload_file_to_s3(file_to_upload)
