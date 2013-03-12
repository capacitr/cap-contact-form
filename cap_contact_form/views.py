from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from forms import ContactForm
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

import models

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

    def post(self, *args, **kwargs):

        contact_form = ContactForm(self.request.POST)
        if contact_form.is_valid():

            if not settings.CONTACT_EMAILS:
                raise ImproperlyConfigured

            to = settings.CONTACT_EMAILS

            name = contact_form.cleaned_data.get("name", "newsletter")
            from_email = contact_form.cleaned_data.get("from_email", None)
            phone = self.request.POST.get("phone", "")
            message = contact_form.cleaned_data.get("message", "sign me up for the newsletter")

            message = render_to_string('email.html',  {
                'message' : message, 
                'name' : name,
                'phone' : phone
            })

            message = name + " says\n\r\n\r" + message 

            send_mail('Contact Form', message, from_email, to)

            contact = models.Contact()
            contact.name = name
            contact.email = from_email
            contact.message = message
            contact.save()

            messages.add_message(self.request, messages.INFO, 'Your email has been sent.')

        else:
            messages.add_message(self.request, messages.INFO, 'You didn\'t fill out the form correctly.')

        if self.request.POST.get("next", None):
            return redirect(self.request.POST.get("next"))

        return redirect(request.META["HTTP_REFERER"])

def send_html_email(from_email, to, subject, message):
    msg = EmailMultiAlternatives(subject, message, from_email, [to])
    msg.attach_alternative(email_body, "text/html")
    return msg.send()

