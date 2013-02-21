# Create your views here.

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

    def post(self, *args, **kwargs):

        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():

            to = settings.CONTACT_EMAILS

            name = contact_form.cleaned_data.get("name", None)
            from_email = contact_form.cleaned_data.get("from", None)
            message = contact_form.cleaned_data.get("message", None)

            message = render_to_string('email.html',  {
                'message' : message, 
                'name' : name
            })

            send_mail('Contact Form', message, from_email, to)

            messages.add_message(self.request, messages.INFO, 'Your email has been sent.')
            return redirect(reverse('contact_us'))


