# Uncomment the imports below before you add the function code
import requests  # Added to enable API calls
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve backend API URLs from .env file
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Function to make GET requests to the backend API.

    Args:
        endpoint (str): The API endpoint to be requested.
        kwargs: URL parameters to be passed as query strings.

    Returns:
        JSON response from the backend API.
    """
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

def analyze_review_sentiments(text):
    """
    Function to analyze sentiment using the deployed microservice.

    Args:
        text (str): The text to analyze.

    Returns:
        JSON response containing sentiment analysis.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"Calling sentiment analyzer at {request_url}")

    try:
        # Call get method of requests library with URL
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"sentiment": "neutral"}

def post_review(data_dict):
    """
    Function to post a review to the backend.

    Args:
        data_dict (dict): Dictionary containing review data.

    Returns:
        JSON response from the backend.
    """
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url}")

    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"status": "failed"}