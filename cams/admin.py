from django.contrib import admin
from .models import (
     UserProfile, CustomUser,
     # Assuming workerProfile is a model
    Booking, Rating, ContactMessage,WorkerProfile,Service
)


#Contact admin
from .models import ContactMessage
from django.contrib.admin import DateFieldListFilter

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'sent_at')
    search_fields = ('name', 'phone')
    list_filter = (('sent_at', DateFieldListFilter),)

## Register CustomUser and related models
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(Rating)
admin.site.register(WorkerProfile)
admin.site.register(Service)
