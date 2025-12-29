from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from cams.models import Booking  # adjust if needed

class Command(BaseCommand):
    help = 'Send booking reminders to users and workers'

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now().date() + timedelta(days=1)
        bookings = Booking.objects.filter(date=tomorrow)

        for booking in bookings:
            # Send to user
            send_mail(
                subject='Booking Reminder',
                message=f"Dear {booking.name}, this is a reminder for your booking on {booking.date}.",
                from_email=None,
                recipient_list=[booking.user.email]
            )
            # Send to worker
            if booking.worker.user.email:
                send_mail(
                    subject='Service Booking Reminder',
                    message=f"Hello {booking.worker.name}, you have a service scheduled for {booking.date}.",
                    from_email=None,
                    recipient_list=[booking.worker.user.email]
                )

        self.stdout.write(f'{bookings.count()} reminder emails sent.')