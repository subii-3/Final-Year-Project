from django.urls import path
from cams import views
from .views import Signup, Home,Login,About,WorkerDashboard,UserDashboard,services_list,Mechanic_Services,Electrician_Services
from .views import Appliances,Home_Renovation,Moving_Storage,Security_Services,Cleaning_Services,Message,contact_view,Book_now
from django.contrib.auth import views as auth_views
from .views import service_detail
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home, name='Home'),
    path('SignUp/',views.Signup,name='SignUp'),
    path('Login/',views.Login, name='Login'),
    path('user/dashboard/', views.UserDashboard, name='UserDashboard'),
    path('worker/dashboard/', views.WorkerDashboard, name='WorkerDashboard'),
    path('Services/', views.services_list, name='Services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('Appliances/', views.Appliances, name='Appliances'),
    path('Home_Renovation/', views.Home_Renovation, name='Home_Renovation'),
    path('Moving_Storage/', views.Moving_Storage, name='Moving_Storage'),
    path('Security_Services/', views.Security_Services, name='Security_Services'),
    path('Mechanic_Services/', views.Mechanic_Services, name='Mechanic_Services'),
    path('Electrician_Services/', views.Electrician_Services, name='Electrician_Services'),
    path('Cleaning_Services/', views.Cleaning_Services, name='Cleaning_Services'),
    path('About', views.About, name='About'),
    path('contact/', contact_view, name='Contact'),
    path('Message', views.Message, name='Message'),
    path('forget-password/', views.ForgotPasswordView.as_view(), name='forget_password'),
    path('reset/<str:token>/', views.ResetPasswordView.as_view(), name='reset_password'),

    path('Book_now/', views.Book_now, name='Book_now'),

    path('book/', views.create_booking, name='create_booking'),
     path('book/<int:worker_id>/', views.create_booking_with_worker, name='create_booking_with_worker'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('submit-booking/', views.submit_booking, name='submit_booking'),
    
    path('worker-profile-form/', views.worker_profile_form, name='worker_profile_form'),

    path('submit_booking/', views.submit_booking, name='submit_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
