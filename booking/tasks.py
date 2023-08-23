from io import BytesIO
# from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from booking.models import Booking, Passenger



# @shared_task
def payment_completed(booking_id, passenger_id):
    """
    Task to send an email notification when an order is successfully paid
    :param order_id:
    :return:
    """
    passenger = Passenger.objects.get(id=passenger_id)
    booking = Booking.objects.get(id=booking_id)
    # Create invoice -email
    # Todo: Check how to translate formated text and the invoice
    subject = f'Blue Airlines Ticket. {booking.id}'
    message = 'Please, find attached tickedt for your booking'
    email = EmailMessage(subject,
                         message,
                         'reubensleeq@gmail.com',
                         [passenger.email])

    # generate PDF
    html = render_to_string('pdf.html', {'booking': booking})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach pdf file
    email.attach(f'booking{booking.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    email.send()
    print("mail sent")


