import boto3
import json

def is_related_to_economy(body):
    """
    Uses Amazon Nova Micro to filter news titles.
    Returns: True if related to US Economy, False otherwise.
    """
    NOVA_MODEL_ID = "eu.amazon.nova-micro-v1:0"
    bedrock_runtime = boto3.client('bedrock-runtime', region_name="eu-west-1")
    # Nova models accept a specific system prompt structure
    system_prompt = (
        "You are a news classifier. "
        "Your task is to analyze the user's news title and determine if it "
        "loosely relates to one or more of the following: Economy, Stock Market, Financial Policy, Business, Prices, Inflation, Markets, Commodities, Incomes, Tax, Crypto, GDP, Employment, Trade."
        "If you are not sure, default to YES."        
        "Respond with ONLY one word: 'YES' or 'NO'."
    )

    # Nova request payload structure
    payload = {
        "system": [{"text": system_prompt}],
        "messages": [
            {
                "role": "user", 
                "content": [{"text": f"Title: {body}"}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 5,  # We only need a short YES/NO response
            "temperature": 0.0    # Set to 0 for deterministic (consistent) results
        }
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=NOVA_MODEL_ID,
            body=json.dumps(payload)
        )
        
        # Parse Nova response body
        response_body = json.loads(response.get('body').read())
        
        # Navigate the Nova output structure
        # output -> message -> content -> list -> text
        model_answer = response_body["output"]["message"]["content"][0]["text"]
        
        # Clean and check answer
        clean_answer = model_answer.strip().upper()
        return "YES" in clean_answer

    except Exception as e:
        print(f"Error checking title '{body}': {e}")
        return False

def get_sentiment(body):
    """
    Uses Amazon Nova Micro to analyze sentiment regarding the US Administration.
    Returns: 
        0 if NO (Not positive)
        1 if YES (Positive)
    """
    NOVA_MODEL_ID = "eu.amazon.nova-micro-v1:0"
    bedrock_runtime = boto3.client('bedrock-runtime', region_name="eu-west-1")
    if not body:
        return None
        
    # Truncate to a reasonable limit for the context window if needed
    truncated_body = body[:10000]

    system_prompt = (
        "You are a political analyst. "
        "Read the provided article text and answer the following question: "
        "'Is the article more positive or negative considering the current/future state of the US economy? Be sure to consider both explicit statements and implicit tones.'"
        "Respond with ONLY one of the following words: 'POSITIVE', 'NEGATIVE'. "
        "Do not provide any explanation."
    )

    payload = {
        "system": [{"text": system_prompt}],
        "messages": [
            {
                "role": "user", 
                "content": [{"text": f"Article Text: {truncated_body}"}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 5,
            "temperature": 0.0
        }
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=NOVA_MODEL_ID,
            body=json.dumps(payload)
        )
        
        response_body = json.loads(response.get('body').read())
        model_answer = response_body["output"]["message"]["content"][0]["text"]
        clean_answer = model_answer.strip().upper()
        
        # Map text answer to integer
        if "POSITIVE" in clean_answer:
            return 1
        else:
            return 0 # Defaults to Negative for "NO" or other outputs

    except Exception as e:
        print(f"Bedrock Sentiment Error: {e}")
        return None