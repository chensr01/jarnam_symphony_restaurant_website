from django.contrib import admin

# Register your models here.
from .models import Reservation, Item, Review

admin.site.register(Reservation)
admin.site.register(Item)
admin.site.register(Review)