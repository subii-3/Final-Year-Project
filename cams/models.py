from django.db import models
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

    
#Contact Message
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

# Extending the default user model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime, timedelta
import uuid

class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    # ✅ Override the default email field to make it unique
    email = models.EmailField(unique=True)

    def generate_reset_token(self):
        self.reset_token = str(uuid.uuid4())
        self.token_expiry = datetime.now() + timedelta(minutes=15)
        self.save()
        return self.reset_token

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

class YourModel(models.Model):
    your_field = models.CharField(max_length=100, default='YourDefaultValue')







class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Updated', 'Updated'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    worker = models.ForeignKey('WorkerProfile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    date = models.DateField()
    time = models.DateTimeField(default=timezone.now)
    service = models.TextField()
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking by {self.name} for {self.worker}"



class Rating(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    stars = models.IntegerField()
    comment = models.TextField()

    
    
    #9.30
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name
        
    

    


class WorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='workerprofile')  # Link with login user
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20,default='N/A')
    location = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='worker_images/')

    def __str__(self):
        return self.name
     
#Services catogory
 


    