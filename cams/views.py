#main page rendering
def Home(request):
    return render(request,'Home.html')
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .models import *

#maris

from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .models import *
from .models import  CustomUser, WorkerProfile, Service ,Booking,Rating
from datetime import datetime, timedelta


from .forms import CustomUserCreationForm ,WorkerProfileForm, ContactForm, BookingForm,RatingForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

# Signup
def Signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'SignUp.html', {'form': form})

#Login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser

def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('userType')

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, 'Login.html')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            print("✅ Authenticated:", user.username)
            print("user_type:", user_type)
            print("user.is_user:", user.is_user)
            print("user.is_worker:", user.is_worker)

            login(request, user)

            if user_type == "worker" and user.is_worker:
                return redirect('WorkerDashboard')
            elif user_type == "user" and user.is_user:
                return redirect('UserDashboard')
            else:
                messages.error(request, "User type mismatch.")
        else:
            messages.error(request, "Incorrect password.")
            
    return render(request, 'Login.html')


def WorkerDashboard(request):
    return render(request,'WorkerDashboard.html')
def UserDashboard(request):
    return render(request,'UserDashboard.html')
def About(request):
    return render(request,'About.html')
def Contact(request):
    return render(request,'Contact.html')

def Services(request):
    return render(request,'Services.html')
def Appliances(request):
    return render(request,'Appliances.html')
def Cleaning_Services(request):
    return render(request,'Cleaning_Services.html')
def Electrician_Services(request):
    return render(request,'Electrician_Services.html')
def Home_Renovation(request):
    return render(request,'Home_Renovation.html')
def Mechanic_Services(request):
    return render(request,'Mechanic_Services.html')
def Moving_Storage(request):
    return render(request,'Moving_Storage.html')
def Security_Services(request):
    return render(request,'Security_Services.html')
def Message(request):
    return render(request,'Message.html')

from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Message.html')  # success page
    else:
        form = ContactForm()

    return render(request, 'Contact.html', {'form': form})


def Book_now(request):
    return render(request,'Book_now.html')

#services

from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import CustomUser as User  # Use your actual model

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forget_password.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()

        print("Input email:", email)
        print("All emails in DB:", list(User.objects.values_list('email', flat=True)))

        user = User.objects.filter(email__iexact=email).first()

        if user:
            token = user.generate_reset_token()  # Ensure this method exists
            reset_link = f"http://127.0.0.1:8000/reset/{token}/"

            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, "Reset link sent to your email.")
        else:
            messages.error(request, "No account found with that email.")
        return redirect('forget_password')

class ResetPasswordView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(reset_token=token)
            if not user.token_expiry or timezone.now() > user.token_expiry:
                messages.error(request, "Token expired. Request a new one.")
                return redirect('forget_password')
            return render(request, 'reset_password.html', {'token': token})
        except User.DoesNotExist:
            messages.error(request, "Invalid reset token.")
            return redirect('forget_password')

    def post(self, request, token):
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect(f'/reset/{token}/')

        try:
            user = User.objects.get(reset_token=token)
            if not user.token_expiry or timezone.now() > user.token_expiry:
                messages.error(request, "Token expired. Request a new one.")
                return redirect('forget_password')

            user.password = make_password(password)
            user.reset_token = None
            user.token_expiry = None
            user.save()
            messages.success(request, "Password reset successful. Please log in.")
            return redirect('/Login/')
        except User.DoesNotExist:
            messages.error(request, "Invalid reset token.")
            return redirect('forget_password')
        
@csrf_protect
@login_required
def mark_booking_completed(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Only allow the worker assigned to this booking to mark it completed
    if booking.worker.user == request.user:
        booking.status = 'Completed'
        booking.save()
        messages.success(request, "Booking marked as completed.")
    else:
        messages.error(request, "You are not authorized to complete this booking.")

    return redirect('WorkerDashboard')

@login_required
def UserDashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    user_bookings = Booking.objects.filter(user=request.user).select_related('worker')


    if request.method == 'POST' and 'booking_id' in request.POST:
        booking_id = request.POST.get('booking_id')
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')

        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        # Update date and time
        booking.date = new_date
        # Combine new date and new time into a full datetime
        booking.time = timezone.make_aware(
        datetime.combine(datetime.strptime(new_date, "%Y-%m-%d").date(), datetime.strptime(new_time, "%H:%M").time()))
        booking.status = 'Updated'
        booking.save()

        messages.success(request, "Booking updated successfully. Worker will be notified.")
        return redirect('UserDashboard')

    return render(request, 'UserDashboard.html', {'bookings': bookings})


#cancle_booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()  # or set a status field like 'Cancelled' if you want to keep record
    return redirect('UserDashboard')



@login_required
def WorkerDashboard(request):
    try:
        worker = WorkerProfile.objects.get(user=request.user)
    except WorkerProfile.DoesNotExist:
        return redirect('worker_profile_form')  # Redirect to user dashboard if not a worker

    all_bookings = Booking.objects.filter(worker=worker).order_by('-created_at')
    updated_bookings = all_bookings.filter(status='Updated')

    return render(request, 'WorkerDashboard.html', {
        'bookings': all_bookings,
        'updated_bookings': updated_bookings,
    })
def Book_now(request):
    return render(request,'Book_now.html')

def worker_profile_form(request):
    # your logic here
    return render(request, 'worker_profile_form.html')
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # logged-in user
            booking.save()
            return redirect('dashboard')  # Change to your actual dashboard route
    else:
        form = BookingForm()
    return render(request, 'book_now.html', {'form': form})

@login_required
def create_booking_with_worker(request, worker_id):
    worker = get_object_or_404(CustomUser, id=worker_id, is_worker=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # logged-in user
            booking.worker = worker  # Pre-select the worker
            booking.save()
            return redirect('dashboard')  # Redirect to a dashboard or booking confirmation page
    else:
        form = BookingForm(initial={'worker': worker})  # Pre-fill the worker in the form

    return render(request, 'book_now.html', {'form': form, 'worker': worker})



@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).select_related('worker')
    return render(request, 'dashboard.html', {'bookings': bookings})


#for booking purpose

def submit_booking(request):
    if request.method == 'POST':
        user = request.user
        worker_id = request.POST.get('worker_id')
        name = request.POST.get('name')
        date = request.POST.get('date')
        service = request.POST.get('service')

        # Assuming you have a Booking model
        Booking.objects.create(
            user=user,
            worker_id=worker_id,
            name=name,
            date=date,
            service=service
        )
        return redirect('UserDashboard')  # Or any success page


    


def worker_profile_form(request):
    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            worker_profile = form.save(commit=False)
            worker_profile.user = request.user
            worker_profile.save()
            return redirect('WorkerDashboard')  # or any page you want
    else:
        form = WorkerProfileForm()
    return render(request, 'worker_profile_form.html', {'form': form})

#worker_profile_list

 

# Main Services Page - shows all 7 services
def services_list(request):
    services = Service.objects.all()
    return render(request, 'Services.html', {'services': services})

# Individual Service Detail Page - shows workers for one service
from django.shortcuts import render, get_object_or_404
from .models import Service, WorkerProfile, Rating

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    all_workers = WorkerProfile.objects.filter(service=service)

    # Get location query from GET parameters
    location_query = request.GET.get('location', '').strip()

    if location_query:
        matching_workers = all_workers.filter(location__icontains=location_query)
        other_workers = all_workers.exclude(id__in=matching_workers.values_list('id', flat=True))
    else:
        matching_workers = all_workers
        other_workers = WorkerProfile.objects.none()

    # Attach ratings to each worker
    for worker in all_workers:
        worker.ratings = Rating.objects.filter(booking__worker=worker)

    context = {
        'service': service,
        'workers': all_workers,
        'location_query': location_query,
        'matching_workers': matching_workers,
        'other_workers': other_workers,
    }

    return render(request, 'service_detail.html', context)



@login_required
def submit_booking(request):
    if request.method == 'POST':
        worker_id = request.POST.get('profile_id')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        date = request.POST.get('date')
        service = request.POST.get('service')

        worker = WorkerProfile.objects.get(id=worker_id)
        user = request.user  # if user is your custom user model

        Booking.objects.create(
            user=user,
            worker=worker,
            name=name,
            contact=contact,
            address=address,
            date=date,
            service=service
        )
        return redirect('booking_success')
    return redirect('Home')


def booking_success(request):
    return render(request, 'booking_success.html')

 



#ratings
@login_required
def submit_rating(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST' and not hasattr(booking, 'rating'):
        Rating.objects.create(
            booking=booking,
            stars=int(request.POST['stars']),
            comment=request.POST['comment']
        )
    return redirect('UserDashboard')

@login_required
def UserDashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    user_bookings = Booking.objects.filter(user=request.user).select_related('worker')

    if request.method == 'POST' and 'booking_id' in request.POST:
        booking_id = request.POST.get('booking_id')
        new_date = request.POST.get('date')
        new_time = request.POST.get('time')

        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        try:
            new_datetime = timezone.make_aware(
                datetime.combine(
                    datetime.strptime(new_date, "%Y-%m-%d").date(),
                    datetime.strptime(new_time, "%H:%M").time()
                )
            )
        except ValueError:
            messages.error(request, "Invalid date/time format.")
            return redirect('UserDashboard')

        booking.date = new_date  # or use new_datetime if you want
        booking.time = new_datetime
        booking.status = 'Updated'
        booking.save()

        messages.success(request, "Booking updated successfully. Worker will be notified.")
        return redirect('UserDashboard')

    # your usual GET request handling code here, e.g.
    context = {'bookings': bookings, 'user_bookings': user_bookings}
    return render(request, 'UserDashboard.html', context)




