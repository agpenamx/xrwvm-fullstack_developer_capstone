# ✅ Import required modules
import requests  # ✅ Added to enable API calls
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Retrieve backend API URLs from .env file (Fixed Double Slash Issue)
backend_url = os.getenv('backend_url', default="http://localhost:3030").rstrip("/")  # ✅ Ensure no trailing slash
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/").rstrip("/")  # ✅ Ensure no trailing slash

# ✅ Improved GET Request Handling (deep seek change )
def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Network exception:", e)
    return response.json()
   
    """
    Function to make GET requests to the backend API.

    Args:
        endpoint (str): The API endpoint to be requested.
        kwargs: URL parameters to be passed as query strings.

    Returns:
        JSON response from the backend API.
    """
    # ✅ Fix: Ensure `state` is explicitly passed
    if "state" in kwargs and kwargs["state"] == "All":
        del kwargs["state"]  # ✅ Remove `state` parameter if "All" is selected

    params = "&".join(f"{key}={value}" for key, value in kwargs.items()) if kwargs else ""
    
    request_url = f"{backend_url}/{endpoint}?{params}".rstrip("?")  # ✅ Ensure proper URL formatting
    print(f"🔍 GET from {request_url}")  # ✅ Debugging log to verify request

    try:
        response = requests.get(request_url)

        if response.status_code != 200:
            print(f"⚠️ Backend returned {response.status_code}: {response.text}")
            return {"error": f"Backend returned {response.status_code}", "details": response.text}
        
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Invalid JSON received from backend at {request_url}")
        return {"error": "Invalid JSON received from backend"}
    except requests.exceptions.RequestException as err:
        print(f"❌ Network Exception: {err}")
        return {"error": f"Request failed: {str(err)}"}

# ✅ FIXED `analyze_review_sentiments` Function
def analyze_review_sentiments(text):
    # ✅ FIXED: Use environment variable
    url = os.getenv('sentiment_analyzer_url') + "/analyze/" + text
    return get_request(url)
    """
    Function to analyze sentiment using the deployed microservice.

    Args:
        text (str): The text to analyze.

    Returns:
        JSON response containing sentiment analysis.
    """
    request_url = f"{sentiment_analyzer_url}/analyze/{text}"
    print(f"🔍 Calling sentiment analyzer at {request_url}")

    try:
        response = requests.get(request_url)

        if response.status_code != 200:
            print(f"⚠️ Sentiment Analyzer returned {response.status_code}: {response.text}")
            return {"error": f"Sentiment Analyzer error {response.status_code}", "details": response.text}

        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Invalid JSON from Sentiment Analyzer at {request_url}")
        return {"sentiment": "neutral", "error": "Invalid JSON response"}
    except requests.exceptions.RequestException as err:
        print(f"❌ Network Exception: {err}")
        return {"sentiment": "neutral", "error": f"Request failed: {str(err)}"}

# ✅ Improved POST Request Handling
def post_review(data_dict):
    """
    Function to post a review to the backend.

    Args:
        data_dict (dict): Dictionary containing review data.

    Returns:
        JSON response from the backend.
    """
    request_url = f"{backend_url}/insert_review"
    print(f"🔍 POST to {request_url}")

    try:
        response = requests.post(request_url, json=data_dict)

        if response.status_code != 200:
            print(f"⚠️ Backend returned {response.status_code}: {response.text}")
            return {"error": f"Backend error {response.status_code}", "details": response.text}

        print(f"✅ POST Response: {response.json()}")
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"❌ Invalid JSON response from backend at {request_url}")
        return {"status": "failed", "error": "Invalid JSON response"}
    except requests.exceptions.RequestException as err:
        print(f"❌ Network Exception: {err}")
        return {"status": "failed", "error": f"Request failed: {str(err)}"}