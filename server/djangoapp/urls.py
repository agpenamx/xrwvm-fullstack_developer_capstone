from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # ✅ Import views properly

app_name = 'djangoapp'

urlpatterns = [
    # ✅ Fetch all dealerships
    path('get_dealers/', views.get_dealerships, name='get_dealers'),

    # 🔧 SUGGESTION: To support filtering by state via URL, ensure that your Django view
    # accepts an optional state parameter. If not, consider adding an additional route:
    # path('get_dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),

    # ✅ Fetch dealer details by ID
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # ✅ Fetch dealer reviews by ID
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),

    # ✅ Add a review
    path('add_review/', views.add_review, name='add_review'),

    # ✅ User authentication endpoints
    path('register/', views.register_user, name='register'),  # 🔥 FIXED function name
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # ✅ Fetch car models
    path('get_cars/', views.get_cars, name='get_cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 🔧 REMINDER: Ensure that any changes in URL patterns are reflected in your front-end code.
# For example, if you add a new route for filtering dealerships by state, update the fetch URL accordingly.