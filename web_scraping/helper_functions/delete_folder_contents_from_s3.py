import boto3
s3 = boto3.client('s3', region_name= "eu-west-1")  # Ireland region

def delete_folder_contents_from_s3(bucket_name, file_key):
    """Deletes a specified file from an S3 bucket.
    Args:
        bucket_name (str): Name of the S3 bucket.
        file_key (str): The key (path) of the file to delete in the S3 bucket."""
    while True:
        # 1. List the objects (max 1000 at a time)
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=file_key)
        
        # If folder is empty, 'Contents' key won't exist
        if 'Contents' not in response:
            break
            
        # 2. Prepare the list of keys to delete
        objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
        
        # 3. Delete them
        s3.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objects_to_delete}
        )
        
        print(f"Deleted batch of {len(objects_to_delete)} files...")

        # 4. If there are no more files to fetch, stop loop
        if not response.get('IsTruncated'):
            break

    print("Folder cleared.")