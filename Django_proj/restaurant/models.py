from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Assuming that you have already extended the User model with a OneToOne link to a Profile model.

# class User(models.Model):
#     user_name = models.CharField(max_length=20)
#     passward = models.CharField(max_length=200)
#     confirm_password  = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=20)
#     first_name = models.CharField(max_length=20)
#     email = models.CharField(max_length=50)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)


class Timeslot(models.Model):
    start_time = models.TextField()
    end_time = models.TextField()


class Table(models.Model):
    table_name= models.TextField()
    capacity = models.IntegerField(validators=[MinValueValidator(1)])


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    creation_time = models.DateTimeField()
    # party_number = models.IntegerField(validators=[MinValueValidator(1)])

class Item(models.Model):
    name = models.CharField(max_length=50)  
    pic = models.ImageField(blank=True)  
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50,default='entree')  
    # Automatically calculate average rating.

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        else:
            return None

    
class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="review_creators")
    creation_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.rating} - {self.item.name}"
 


    
    
    
    