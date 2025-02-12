# Uncomment the following imports before adding the Model code
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# 🚀 Car Make Model: Represents the manufacturer details
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # 🏭 Manufacturer Name
    description = models.TextField()  # 📝 Manufacturer Description

    # 🔹 __str__ method to return CarMake name
    def __str__(self):
        return self.name  # 📌 Displays Car Make name in admin panel

# 🚀 Car Model: Represents specific car details
# <HINT> Create a Car Model model `class CarModel(models.Model)`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # 🔗 Many-to-One relation with CarMake
    name = models.CharField(max_length=100)  # 🚗 Model Name

    # 🚘 Define Car Types
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),  # 🚀 Added optional category
    ]
    
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')  # 🚘 Car Type selection

    # 📅 Year field with validation
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),  # 🚀 Prevents future years
            MinValueValidator(2015)   # 🚀 Ensures valid car model years
        ]
    )

    # 🔹 __str__ method to display Car Make & Model
    def __str__(self):
        return f"{self.car_make.name} {self.name}"  # 📌 Example: "Toyota Corolla"