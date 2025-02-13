# ✅ Import required modules
from django.shortcuts import render
from django.http import JsonResponse
import json
import logging
import requests  # ✅ Required for API calls
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CarMake, CarModel  
from .populate import initiate  
from .restapis import get_request, analyze_review_sentiments, post_review  

# ✅ Logger setup
logger = logging.getLogger(__name__)

# ✅ Authentication Functions
@csrf_exempt
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')

        # 🔧 Ensure username and password keys match frontend request
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "error": "Invalid credentials"}, status=401)
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        return JsonResponse({"error": "An error occurred while logging in"}, status=500)

def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def register_user(request):  # ✅ Changed from `registration` to `register_user`
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')

        if not username or not password:
            return JsonResponse({"error": "Missing username or password"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)

        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        return JsonResponse({"error": "An error occurred while registering"}, status=500)

# ✅ Fetch Car Models & Makes
def get_cars(request):
    try:
        count = CarMake.objects.count()
        if count == 0:
            initiate()  # 🔧 Populate database if empty
        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        logger.error(f"❌ Error fetching car models: {e}")
        return JsonResponse({"error": "Failed to retrieve cars"}, status=500)

# ✅ Fetch Dealerships with Authentication & JSON Validation
def get_dealerships(request, state="All"):
    """
    Fetches all dealerships from the backend API.
    - Ensures authentication by using session cookies.
    - If authentication fails, returns a proper error.
    - Prevents JSONDecodeError by verifying content type.
    """
    session = requests.Session()  # ✅ Create session for cookies

    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"

    headers = {}  # ✅ Prepare headers

    # 🔧 FIX: Properly handle authentication
    if request.user.is_authenticated:
        session_cookies = request.COOKIES
        headers["Cookie"] = "; ".join([f"{key}={value}" for key, value in session_cookies.items()])
        logger.debug(f"🔍 Using session cookies: {headers['Cookie']}")  
    else:
        logger.error("❌ User is not authenticated. Access denied.")
        return JsonResponse({"error": "User not authenticated", "status": 403})

    try:
        response = session.get(f"http://127.0.0.1:8888{endpoint}", headers=headers)

        # ✅ LOG response headers and content for debugging
        logger.debug(f"🔍 Response Status: {response.status_code}")
        logger.debug(f"🔍 Response Headers: {response.headers}")
        logger.debug(f"🔍 Response Content (First 500 chars): {response.text[:500]}")  

        # 🔧 FIX: If response is not JSON, handle it
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            logger.error("❌ API did not return JSON. Possible OAuth issue.")
            return JsonResponse({"status": 500, "error": "Backend returned non-JSON response. Check authentication."})

        # ✅ Now we are sure it's JSON, so we can safely parse it
        return JsonResponse({"status": 200, "dealers": response.json()})

    except requests.exceptions.JSONDecodeError as json_err:
        logger.error(f"❌ JSON Decode Error: {json_err}")
        return JsonResponse({"status": 500, "error": "Invalid JSON received from backend"})

    except requests.exceptions.RequestException as req_err:
        logger.error(f"❌ Network Exception: {req_err}")
        return JsonResponse({"status": 500, "error": f"Request failed: {str(req_err)}"})

# ✅ Fetch dealer details by ID
def get_dealer_details(request, dealer_id):
    try:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)

        logger.debug(f"🔍 Fetching dealer details for ID: {dealer_id} -> Response: {dealership}")

        if not dealership:
            return JsonResponse({"status": 404, "error": "Dealer not found"})

        return JsonResponse({"status": 200, "dealer": dealership})
    except Exception as e:
        logger.error(f"❌ Error fetching dealer details: {e}")
        return JsonResponse({"status": 500, "error": "Failed to retrieve dealer details"})

# ✅ Fetch dealer reviews by ID
def get_dealer_reviews(request, dealer_id):
    try:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        logger.debug(f"🔍 Fetching dealer reviews for ID: {dealer_id} -> Response: {reviews}")

        if not reviews:
            return JsonResponse({"status": 404, "error": "No reviews found for this dealer"})

        # 🔧 Process each review to add sentiment using the sentiment analyzer service
        for review in reviews:
            response = analyze_review_sentiments(review['review'])
            review['sentiment'] = response.get('sentiment', "neutral")

        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as e:
        logger.error(f"❌ Error fetching dealer reviews: {e}")
        return JsonResponse({"status": 500, "error": "Failed to retrieve reviews"})

# ✅ Add a dealer review
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    
    try:
        data = json.loads(request.body)
        response = post_review(data)

        logger.debug(f"🔍 Submitting review: {data} -> Response: {response}")

        if not response:
            return JsonResponse({"status": 500, "message": "Failed to submit review"})

        return JsonResponse({"status": 200, "response": response})
    except Exception as e:
        logger.error(f"❌ Error submitting review: {e}")
        return JsonResponse({"status": 500, "message": f"Error: {str(e)}"})