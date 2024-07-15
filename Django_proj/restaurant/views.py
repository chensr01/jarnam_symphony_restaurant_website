from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Reservation, Table, Timeslot, Item, Review
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import threading
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.http import HttpResponseBadRequest
from datetime import timedelta
from .forms import ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.
def home(request):
    return render(request, 'restaurant/home.html')

def about(request):
    return render(request, 'restaurant/about.html')

def reservation(request):
    timeslots = Timeslot.objects.all()
    if request.user.is_authenticated:
        return render(request, 'restaurant/reservation.html', {'timeslots': timeslots})
    else:
        return login_reservation(request)

def menu(request):
    return render(request, 'restaurant/menu.html')

def me(request):
    if request.user.is_authenticated:
        today = timezone.localdate() 

        reservations = Reservation.objects.filter(user=request.user, creation_time__date=today)
        return render(request, 'restaurant/me.html', {'reservations': reservations})
    else:
        return login_me(request)
    
def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if reservation.user == request.user:  
        reservation.delete()
    return me(request) 

def image_upload(request):
    profile_instance = request.user.profile
    
    if request.method == 'POST':

        form = ProfileImageForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            if 'picture' in request.FILES:
                profile_instance.picture= form.cleaned_data['picture']
            form.save()
            render(request, 'restaurant/me.html')
        else:
            # If the form is not valid, include the form in the context to display errors
            context = {'form': form}
            return render(request, 'restaurant/me.html', context)

    context = {'form': form}
    return render(request, 'restaurant/me.html', context)

def get_photo(request, user_id):
    item = get_object_or_404(Profile, user_id=user_id)

    if not item.picture:
        raise Http404
    return HttpResponse(item.picture)

def login_me(request):
    request.session['login_redirect'] = 'me'
    return render(request, 'restaurant/login_me.html')

def login_reservation(request):
    request.session['login_redirect'] = 'reservation'
    return render(request, 'restaurant/login_reservation.html')

def logout_action(request):
    logout(request)
    return redirect(reverse('home'))

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'restaurant/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'restaurant/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)

    if request.session.get('login_redirect') == 'me':
        del request.session['login_redirect']
        return redirect(reverse('me'))
    elif request.session.get('login_redirect') == 'reservation':
        del request.session['login_redirect']
        return redirect(reverse('reservation'))
    else:
        return redirect(reverse('home'))
    # return redirect(reverse('home'))

@login_required
def update_info(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        # Redirect to some page that confirms the update
        today = timezone.localdate() 

        reservations = Reservation.objects.filter(user=request.user, creation_time__date=today)
        return render(request, 'restaurant/me.html', {'reservations': reservations})

@transaction.atomic
def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'restaurant/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'restaurant/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    
    new_profile = Profile(user=new_user)
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('home'))


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(self.email)
        except Exception as e:
            print("An error occurred while sending the email:", str(e))
            if hasattr(e, 'to_dict'):
                print("Error details:", e.to_dict)  # Assuming to_dict is a property, not a method
            else:
                print("No detailed error information available.")

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

def get_reservation(request, timeslot_id):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    all_timeslots = [
        "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
        "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
        "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM",
        "07:00 PM", "07:30 PM", "08:00 PM"
    ]

    # Find index of the selected timeslot
    try:
        index = all_timeslots.index(timeslot_id)
    except ValueError:
        return _my_json_error_response("Invalid timeslot provided", status=400)
    
    # Calculate indices for 90 min before and after , ensuring they are valid
    indices = [i for i in range(index - 2, index + 3) if 0 <= i < len(all_timeslots)]
    selected_timeslots = [all_timeslots[i] for i in indices]

    # Filter Timeslots and Reservations
    timeslots = Timeslot.objects.filter(start_time__in=selected_timeslots)
    # Get today's date in the timezone set in settings.py
    today = timezone.localtime(timezone.now()).date()

    reservations = (Reservation.objects
                    .filter(timeslot__in=timeslots, creation_time__date=today)
                    .select_related('table'))


    reservations_data = []
    for r in reservations:
        reservations_data.append({
            'id': r.id,
            'user': r.user.username,
            'timeslot': r.timeslot.start_time,
            'table': r.table.table_name,
        })

    response_data = {
        'reservations': reservations_data,
    }

    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')

def get_reservation_data(request, timeslot_id):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    all_timeslots = [
        "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
        "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
        "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM",
        "07:00 PM", "07:30 PM", "08:00 PM"
    ]

    # Find index of the selected timeslot
    try:
        index = all_timeslots.index(timeslot_id)
    except ValueError:
        return _my_json_error_response("Invalid timeslot provided", status=400)
    
    # Calculate indices for 90 min before and after , ensuring they are valid
    indices = [i for i in range(index - 2, index + 3) if 0 <= i < len(all_timeslots)]
    selected_timeslots = [all_timeslots[i] for i in indices]

    # Filter Timeslots and Reservations
    timeslots = Timeslot.objects.filter(start_time__in=selected_timeslots)
    # Get today's date in the timezone set in settings.py
    today = timezone.localtime(timezone.now()).date()

    reservations = (Reservation.objects
                    .filter(timeslot__in=timeslots, creation_time__date=today)
                    .select_related('table'))


    reservations_data = []
    for r in reservations:
        reservations_data.append({
            'id': r.id,
            'user': r.user.username,
            'timeslot': r.timeslot.start_time,
            'table': r.table.table_name,
        })

    response_data = {
        'reservations': reservations_data,
    }
    return response_data

@transaction.atomic
def make_reservation(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'table_id' in request.POST or not request.POST['table_id'] or not 'timeslot_id' in request.POST or not request.POST['timeslot_id']:
        return _my_json_error_response("You must select a timeslot and a table to make reservation.", status=400)
    
    table_name = request.POST.get('table_id')
    try:
        table = Table.objects.get(table_name=table_name)
    except Table.DoesNotExist:
        return _my_json_error_response("Table not found", status=400)
    
    # Find the Timeslot by start_time
    timeslot_start_str = request.POST.get('timeslot_id')
    try:
        timeslot = Timeslot.objects.get(start_time=timeslot_start_str)
    except Timeslot.DoesNotExist:
        return _my_json_error_response("Timeslot not found", status=400)
    
    # Check if the time now passes previous reservation slot
    time_str = timeslot.start_time
    time_obj = datetime.strptime(time_str, '%I:%M %p').time()
    now = timezone.localtime(timezone.now())
    target_datetime = datetime.combine(now.date(), time_obj, now.tzinfo)

    # if now > target_datetime:
    #     return _my_json_error_response("You must select a time later than now", status=400)

    
    # Check if there's already a reservation for the same table and timeslot for today
    today_date = now.date()
    if Reservation.objects.filter(table=table, timeslot=timeslot, creation_time__date=today_date).exists():
        return _my_json_error_response("A reservation for this table and timeslot already exists today", status=400)
    

    # Create the reservation
    new_reservation = Reservation(user=request.user, timeslot=timeslot, table=table, creation_time=timezone.now())   # Adjust user=None
    new_reservation.save()

    # Send an email to the user
    email = Mail(
        from_email=settings.EMAIL_HOST_USER,
        to_emails=request.user.email,
        subject=f"Reservation Confirmation - {new_reservation.creation_time.strftime('%m/%d/%Y')} {timeslot.start_time} [Confirmation #{new_reservation.id}]",
        html_content=f"Dear {request.user.first_name},<br><br>"
                     f"You have successfully reserved a table of {table.capacity} at "
                     f"{timeslot.start_time} for today. Thank you for your reservation.<br><br>"
                     "At Jarnam Symphony, we strive to offer not just a meal, but an experience that resonates with the harmonious "
                     "symphony of taste and ambiance. Prepare your senses for a culinary journey where each dish is composed like a "
                     "masterpiece of flavors and artistry.<br><br>"
                     "Should your plans change or if you have any special requests, please let us know at (317)585-8468. We are here "
                     "to ensure your dining experience is nothing less than perfect.<br><br>"
                     "We look forward to the pleasure of your company.<br><br>"
                     "Warm regards,<br><br>"
                     "The Jarnam Symphony Team"
    )

    EmailThread(email).start()

    # After creating the reservation, get the updated list
    # return get_reservation(request, timeslot_id=timeslot_start_str)

    reservation_data = get_reservation_data(request, timeslot_id=timeslot_start_str)
    # Combine the success message with the reservation data
    response_data = {'success': "Your reservation was successfully made!"}
    response_data.update(reservation_data)  # Merge the reservation data into the response

    return JsonResponse(response_data, status=200)

#items ordered by category
def menu(request):
    print("Entering menu_view")
    items = Item.objects.all()
    print(items)
    items_by_category = {}
    for item in items:
        if item.category not in items_by_category:
            items_by_category[item.category] = []
        items_by_category[item.category].append(item)
    print(items_by_category) 
    return render(request, 'restaurant/menu.html', {'items_by_category': items_by_category})

def item_detail_view(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    stars_range = range(1, 6) 
    return render(request, 'restaurant/item_detail.html', {'item': item, 'stars_range': stars_range})

def submit_review(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Item, pk=item_id)
            review = Review.objects.create(
                item=item,
                comment=data['comment'],
                rating=data['rating'],
                created_by=request.user,
                creation_time=now()
            )
            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Review added successfully.'})
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except KeyError:
            # Handle missing fields in JSON data
            return HttpResponseBadRequest("Missing required parameters: 'comment' or 'rating'")
        except Exception as e:
            # Catch all other exceptions and return a general error response
            return HttpResponseBadRequest(str(e))
    else:
        # Handle incorrect request method
        return HttpResponseBadRequest("Invalid request method. This endpoint supports only POST requests.")

from django.db.models import Avg

from django.db.models import Avg

def get_reviews(request, item_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(item_id=item_id)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        # Prepare two formats of the average rating
        average_rating_decimal = "{:.2f}".format(average_rating)
        average_rating_integer = int(round(average_rating))

        reviews_data = list(reviews.values('rating', 'comment', 'created_by__username', 'creation_time'))
        reviews_list = [
            {
                'rating': review['rating'],
                'comment': review['comment'],
                'created_by': review['created_by__username'],
                'creation_time': review['creation_time'].strftime("%Y-%m-%d %H:%M:%S")
            } for review in reviews_data
        ]

        response_data = {
            'reviews': reviews_list,
            'average_rating_decimal': average_rating_decimal,
            'average_rating_integer': average_rating_integer
        }
        return JsonResponse(response_data, safe=False)
    else:
        return HttpResponseBadRequest("Invalid request method. This endpoint supports only GET requests.")
