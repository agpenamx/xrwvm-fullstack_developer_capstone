"""
djangoproj URL Configuration

Defines URL patterns for Django, including admin panel, API endpoints, and frontend routes.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views  # ✅ Import views for API endpoints

urlpatterns = [
    # ✅ Admin Panel
    path('admin/', admin.site.urls),

    # ✅ AUTHENTICATION ROUTES (🔧 FIXED: Use views instead of templates)
    path('login/', views.login_user, name='login'),  
    path('register/', views.register_user, name='register'),  
    path('logout/', views.logout_user, name='logout'),  

    # ✅ STATIC PAGES (Frontend HTML templates)
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('', TemplateView.as_view(template_name="Home.html")),  # ✅ Fix for home page

    # ✅ BACKEND API ROUTES (Django Serves JSON Responses)
    path('api/get_dealers/', views.get_dealerships, name='api_get_dealers'),  
    path('api/dealer/<int:dealer_id>/', views.get_dealer_details, name='api_dealer_details'),
    path('api/reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='api_dealer_reviews'),
    path('api/add_review/', views.add_review, name='api_add_review'),

    # ✅ FRONTEND ROUTES (Handled by React)
    path('dealers/', TemplateView.as_view(template_name="Home.html")),  # ✅ FIX: Ensure correct template
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),

    # ✅ React Catch-All Route (Handles React Routing)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='react-app'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)