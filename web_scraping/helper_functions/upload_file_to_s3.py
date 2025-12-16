import boto3
s3 = boto3.client("s3", region_name="eu-west-1")  # Ireland region

def upload_file_to_s3(file_path_local, S3_bucket_name, file_key_s3 ):
    """Uploads a local file to a specified S3 bucket and key.
    Args:
        file_path_local (str): Path to the local file to upload.
        S3_bucket_name (str): Name of the target S3 bucket.
        file_key_s3 (str): S3 key (prefix/name) where the file will be stored."""
    try:
        s3.upload_file(file_path_local, S3_bucket_name, file_key_s3)
        print(f"✅ Success! Uploaded {file_path_local} to s3://{S3_bucket_name}/{file_key_s3}")
    except Exception as e:
        print(f"❌ Error uploading file: {e}")