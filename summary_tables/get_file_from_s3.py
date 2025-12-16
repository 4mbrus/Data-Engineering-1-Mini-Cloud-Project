import pandas as pd
import boto3
import os

s3 = boto3.client("s3", region_name="eu-west-1")  # Ireland region

def fetch_latest_data(bucket_name, folder_prefix, local_filename):
    """Fetches the latest file from a given S3 bucket and folder prefix, downloads it locally.
    Args:
        bucket_name (str): Name of the S3 bucket.
        folder_prefix (str): Folder path prefix in the S3 bucket.
        local_filename (str): Local filename (without extension) to save the downloaded file."""
    # 2. List objects in that folder to find the actual filename
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

    # 3. Find the latest file (ignoring the folder placeholder itself)
    # We sort by 'LastModified' to ensure we get the newest export
    files = response.get('Contents', [])
    # Filter out the folder itself and get files
    data_files = [f for f in files if f['Key'] != folder_prefix]

    if not data_files:
        print("❌ No files found. Did the Athena query finish?")
    else:
        # Get the most recent file
        latest_file = max(data_files, key=lambda x: x['LastModified'])
        file_key = latest_file['Key']
        
        print(f"✅ Found file: {file_key}")
        
        # 4. Download and Load into Python
        # We download to a temporary file first
        s3.download_file(bucket_name, file_key, f"{local_filename}.json.gz")
        
        print("⬇️ Download complete.")
        try:
            # Try reading as JSONL (one JSON object per line)
            temp = pd.read_json(f"{local_filename}.json.gz", compression='gzip', lines=True)
        except (ValueError, pd.errors.JSONDecodeError) as e:
            # If that fails, try reading as a single JSON object
            print(f"⚠️ JSONL parsing failed ({e}), attempting standard JSON parsing...")
            temp = pd.read_json(f"{local_filename}.json.gz", compression='gzip')
        
        temp.to_json(f"{local_filename}.json")  # Save uncompressed for easier reuse
        #delete .gz file after extraction
        os.remove(f"{local_filename}.json.gz")
        print("🗃️ Data loaded into DataFrame and saved locally.")