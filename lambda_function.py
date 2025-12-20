# Trifggered when the source data file is updated in S3.
# Runs Athena queries to refresh views and saves results as CSV files in designated S3 locations.

import boto3
import time
import os

# --- CONFIGURATION ---
ATHENA_DB = 'ambrus' 
BUCKET_NAME = 'business-news-sentiments'
TEMP_OUTPUT_PREFIX = 'athena-temp-results/'

JOBS = [
    {
        "view_name": "monthly_combined_sentiments",
        "target_prefix": "news_sentiments_monthly/sentiment/",
        "final_filename": "monthly_combined_sentiments.csv"
    },
    {
        "view_name": "monthly_topic_breakdown",
        "target_prefix": "news_sentiments_monthly/topic_breakdown/",
        "final_filename": "monthly_topic_breakdown.csv"
    }
]

def lambda_handler(event, context):
    athena = boto3.client('athena')
    s3 = boto3.client('s3')
    
    print("Source file updated. Starting Athena refresh jobs...")

    running_queries = []
    
    # 1. Start all queries
    for job in JOBS:
        print(f"Starting query for view: {job['view_name']}")
        
        temp_output = f"s3://{BUCKET_NAME}/{TEMP_OUTPUT_PREFIX}"
        
        response = athena.start_query_execution(
            QueryString=f"SELECT * FROM \"{job['view_name']}\"",
            QueryExecutionContext={'Database': ATHENA_DB},
            ResultConfiguration={'OutputLocation': temp_output}
        )
        
        job['query_id'] = response['QueryExecutionId']
        running_queries.append(job)

    # 2. Wait for completion and Rename/Move
    while running_queries:
        for job in running_queries[:]: 
            query_id = job['query_id']
            status = athena.get_query_execution(QueryExecutionId=query_id)
            state = status['QueryExecution']['Status']['State']
            
            if state == 'SUCCEEDED':
                print(f"Query SUCCEEDED: {job['view_name']}")
                
                source_key = f"{TEMP_OUTPUT_PREFIX}{query_id}.csv"
                target_key = f"{job['target_prefix']}{job['final_filename']}"
                
                # Copy/Rename
                print(f"Copying to {target_key}...")
                s3.copy_object(
                    Bucket=BUCKET_NAME,
                    CopySource={'Bucket': BUCKET_NAME, 'Key': source_key},
                    Key=target_key
                )
                
                # Cleanup
                s3.delete_object(Bucket=BUCKET_NAME, Key=source_key)
                s3.delete_object(Bucket=BUCKET_NAME, Key=source_key + '.metadata')
                
                running_queries.remove(job)
                
            elif state in ['FAILED', 'CANCELLED']:
                reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown')
                print(f"Query FAILED: {job['view_name']} - Reason: {reason}")
                running_queries.remove(job)
                
        if running_queries:
            time.sleep(2)

    return {
        'statusCode': 200,
        'body': 'All views refreshed and saved as CSV.'
    }