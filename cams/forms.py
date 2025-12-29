from django import forms
from .models import ContactMessage, Booking

from django.contrib.auth.models import User

from .models import Rating



#Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']




class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['worker', 'date', 'time', 'details']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = CustomUser.objects.filter(is_worker=True)


from .models import WorkerProfile

class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ['name', 'contact', 'location', 'experience', 'service', 'image',]

# forms.py custom user

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'is_user', 'is_worker']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
