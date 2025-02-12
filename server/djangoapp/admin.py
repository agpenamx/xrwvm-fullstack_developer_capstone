# Uncomment the following imports before adding the Model code
from django.contrib import admin
from .models import CarMake, CarModel  # Importing the models

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):  # Allows inline editing of CarModel within CarMake
    model = CarModel
    extra = 1  # Number of extra empty forms

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']
    list_filter = ['car_make', 'type']
    search_fields = ['name', 'car_make__name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # Allows CarModel objects to be added directly under CarMake
    list_display = ['name', 'description']
    search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)