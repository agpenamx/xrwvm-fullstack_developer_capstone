# ✅ Import required modules
from django.shortcuts import render
from django.http import JsonResponse
import json
import logging
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

        # 🔧 SUGGESTION: Ensure that the JSON keys 'userName' and 'password' match those sent from the front end.
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "error": "Invalid credentials"}, status=401)
    except Exception as e:
        logger.error(f"Login error: {e}")
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
        logger.error(f"Registration error: {e}")
        return JsonResponse({"error": "An error occurred while registering"}, status=500)

# ✅ Fetch Car Models & Makes
def get_cars(request):
    try:
        count = CarMake.objects.count()
        if count == 0:
            # 🔧 SUGGESTION: This will populate the DB if no CarMake exists.
            initiate()  
        car_models = CarModel.objects.select_related('car_make')
        # 🔧 SUGGESTION: Consider expanding the returned data if needed.
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        logger.error(f"Error fetching car models: {e}")
        return JsonResponse({"error": "Failed to retrieve cars"}, status=500)

# ✅ Fetch Dealerships with State Filtering
def get_dealerships(request, state="All"):
    """
    Fetches all dealerships from the backend API.
    If a state is provided and is not "All", filters dealerships by that state.
    Returns a JSON response.
    """
    # 🔧 SUGGESTION: Use '/fetchDealers' for all dealers; for a specific state, append the state to the endpoint.
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)

    logger.debug(f"Fetching dealers for state: {state} -> Response: {dealerships}")

    if not dealerships:
        return JsonResponse({"status": 500, "error": "No dealerships found or backend API failed."})

    return JsonResponse({"status": 200, "dealers": dealerships})

# ✅ Fetch dealer details by ID (Fixed Definition)
def get_dealer_details(request, dealer_id):
    try:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)

        logger.debug(f"Fetching dealer details for ID: {dealer_id} -> Response: {dealership}")

        if not dealership:
            return JsonResponse({"status": 404, "error": "Dealer not found"})

        return JsonResponse({"status": 200, "dealer": dealership})
    except Exception as e:
        logger.error(f"Error fetching dealer details: {e}")
        return JsonResponse({"status": 500, "error": "Failed to retrieve dealer details"})

# ✅ Fetch dealer reviews by ID (Fixed error handling)
def get_dealer_reviews(request, dealer_id):
    try:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        logger.debug(f"Fetching dealer reviews for ID: {dealer_id} -> Response: {reviews}")

        if not reviews:
            return JsonResponse({"status": 404, "error": "No reviews found for this dealer"})

        # 🔧 SUGGESTION: Process each review to add sentiment using the sentiment analyzer service.
        for review in reviews:
            response = analyze_review_sentiments(review['review'])
            review['sentiment'] = response.get('sentiment', "neutral")

        return JsonResponse({"status": 200, "reviews": reviews})
    except Exception as e:
        logger.error(f"Error fetching dealer reviews: {e}")
        return JsonResponse({"status": 500, "error": "Failed to retrieve reviews"})

# ✅ Add a dealer review
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    
    try:
        data = json.loads(request.body)
        response = post_review(data)

        logger.debug(f"Submitting review: {data} -> Response: {response}")

        if not response:
            return JsonResponse({"status": 500, "message": "Failed to submit review"})

        return JsonResponse({"status": 200, "response": response})
    except Exception as e:
        logger.error(f"Error submitting review: {e}")
        return JsonResponse({"status": 500, "message": f"Error: {str(e)}"})