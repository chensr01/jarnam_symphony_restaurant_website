from django.contrib import admin
from django.urls import path, include
from restaurant import views
from django.shortcuts import redirect

urlpatterns = [
    
    path('', views.home, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('reservation', views.reservation, name='reservation'),
    path('me', views.me, name='me'),
    path('get-reservation/<timeslot_id>/', views.get_reservation, name='get-reservation-with-id'),
    path('make-reservation', views.make_reservation, name='make-reservation'),
    path('login-me', views.login_me, name='login-me'),
    path('login-reservation', views.login_reservation, name='login-reservation'),
    path('item/<int:item_id>/', views.item_detail_view, name='item_detail'),
    path('submit_review/<int:item_id>/', views.submit_review, name='submit_review'),
    path('get_reviews/<int:item_id>/', views.get_reviews, name='get_reviews'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('profile-pic/', views.image_upload, name='profile-pic'),
    path('photo/<int:user_id>/',views.get_photo, name='photo'),
    path('update_info/', views.update_info, name='update_info'),
    path('admin/', admin.site.urls),
]
