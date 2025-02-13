# ✅ Import required modules
from django.shortcuts import render
from django.http import JsonResponse
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests  # ✅ Added to enable API calls
from .models import CarMake, CarModel  
from .populate import initiate  
from .restapis import get_request, analyze_review_sentiments, post_review  

# ✅ Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ✅ Utility function for consistent JSON responses
def json_response(data, status=200):
    return JsonResponse(data, status=status)

# ===== 🔐 Authentication Views =====

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return json_response({"error": "Invalid request method"}, status=400)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        logger.error("❌ JSON decode error in login_user")
        return json_response({"error": "Invalid JSON format"}, status=400)

    username = data.get("userName")
    password = data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        request.session.save()  # ✅ Ensure session is saved

        response = json_response({"userName": username, "status": "Authenticated"})
        response.set_cookie("sessionid", request.session.session_key, httponly=True, samesite='Lax')

        logger.info(f"✅ User '{username}' logged in successfully.")
        return response

    logger.warning(f"❌ Authentication failed for user '{username}'.")
    return json_response({"error": "Invalid credentials"}, status=401)

@csrf_exempt
def logout_user(request):
    if request.method != "POST":
        return json_response({"error": "Invalid request method"}, status=400)
    
    logout(request)
    logger.info("✅ User logged out successfully.")
    return json_response({"userName": ""})

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return json_response({"error": "Invalid request method"}, status=400)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        logger.error("❌ JSON decode error in register_user")
        return json_response({"error": "Invalid JSON format"}, status=400)

    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if User.objects.filter(username=username).exists():
        logger.warning(f"❌ Registration attempt with existing username '{username}'.")
        return json_response({"userName": username, "error": "Already Registered"}, status=409)

    try:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        request.session.save()  # ✅ Ensure session is saved

        response = json_response({"userName": username, "status": "Authenticated"})
        response.set_cookie("sessionid", request.session.session_key, httponly=True, samesite='Lax')

        logger.info(f"✅ User '{username}' registered and authenticated successfully.")
        return response
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        return json_response({"error": "Registration failed"}, status=500)

# ===== 🚗 Fetch Car Models & Makes =====

def get_cars(request):
    try:
        count = CarMake.objects.count()
        if count == 0:
            initiate()  
        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        return json_response({"CarModels": cars})
    except Exception as e:
        logger.error(f"❌ Error fetching car models: {e}")
        return json_response({"error": "Failed to retrieve cars"}, status=500)

# ===== 🏬 Fetch Dealerships & Reviews =====

def get_dealerships(request, state="All"):
    session = requests.Session()
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"

    headers = {}

    if request.user.is_authenticated:
        session_cookies = request.COOKIES
        headers["Cookie"] = "; ".join([f"{key}={value}" for key, value in session_cookies.items()])
        session_id = request.session.session_key
        if session_id:
            headers["Authorization"] = f"Bearer {session_id}"

    try:
        BACKEND_SERVICE_HOST = os.getenv("BACKEND_SERVICE_HOST", "backend-service")
        response = session.get(f"http://{BACKEND_SERVICE_HOST}:8888{endpoint}", headers=headers)

        logger.debug(f"🔍 Response Status: {response.status_code}")
        logger.debug(f"🔍 Response Content: {response.text[:500]}")

        if "application/json" not in response.headers.get("Content-Type", ""):
            return json_response({"status": 500, "error": "Backend did not return JSON. Check authentication."})

        return json_response({"status": 200, "dealers": response.json()})
    except requests.exceptions.RequestException as req_err:
        logger.error(f"❌ Request Exception: {req_err}")
        return json_response({"status": 500, "error": "Request failed"})

# ✅ **Re-added `get_dealer_reviews`**
def get_dealer_reviews(request, dealer_id):
    try:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if not reviews:
            return json_response({"status": 404, "error": "No reviews found for this dealer"})

        for review in reviews:
            response = analyze_review_sentiments(review['review'])
            review['sentiment'] = response.get('sentiment', "neutral")

        return json_response({"status": 200, "reviews": reviews})
    except Exception as e:
        logger.error(f"❌ Error fetching dealer reviews: {e}")
        return json_response({"status": 500, "error": "Failed to retrieve reviews"})

# ===== 📝 Add a Dealer Review =====

@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return json_response({"status": 405, "message": "Method Not Allowed"}, status=405)

    if not request.user.is_authenticated:
        return json_response({"status": 403, "message": "Unauthorized"}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return json_response({"status": 400, "message": "Invalid JSON format"}, status=400)

    try:
        response = post_review(data)

        if not response:
            return json_response({"status": 500, "message": "Failed to submit review"})

        return json_response({"status": 200, "response": response})
    except Exception as e:
        logger.error(f"❌ Error submitting review: {e}")
        return json_response({"status": 500, "message": "Error submitting review"})