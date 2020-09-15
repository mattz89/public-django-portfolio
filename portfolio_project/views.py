from django.shortcuts import render
from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from django.contrib import messages
from twilio.rest import Client
from portfolio_project import lookup


def home(request):
    return render(request, 'landing.html')

def textmatt(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        phone = request.POST['phone']
        valid_check = lookup.is_valid_number(phone)
        message = request.POST['message']
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        if valid_check == True:
            for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
                if recipient:
                    client.messages.create(to=recipient,
                                        from_=settings.TWILIO_NUMBER,
                                        body="Name: " + first_name + "\n" + "Phone: " + phone + "\n" + "Message: " + message)
                    client.messages.create(to=phone,
                                        from_=settings.TWILIO_NUMBER,
                                        body="Hi " + first_name + "! Thanks for reaching out. I have receieved your text message, and I'll be in touch soon.\n -Matt Z")
        else:
            return HttpResponse("Sorry, please go back and enter a valid phone number to text Matt", 200)
        return HttpResponse("Thank you. Your text has been sent!", 200)
