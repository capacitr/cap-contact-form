# Create your views here.

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from forms import ContactForm
from django.core.urlresolvers import reverse
from django.conf import settings

class ContactUsView(TemplateView):
    template_name = 'contact_us.html'

    def post(self, *args, **kwargs):

        contact_form = ContactForm(self.request.POST)
        if contact_form.is_valid():

            to = settings.CONTACT_EMAILS

            name = contact_form.cleaned_data.get("name", "newsletter")
            from_email = contact_form.cleaned_data.get("from_email", None)
            message = contact_form.cleaned_data.get("message", "sign me up for the newsletter")

            message = render_to_string('email.html',  {
                'message' : message, 
                'name' : name
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

        return redirect(reverse('contact_us'))

def get_form(request, form_slug):
    form = get_object_or_404(Form, slug=form_slug)

    c = {
        "slug" : form.slug,
        "message" : form.message,
        "source" : form.form_type
        }
    return render(request, form.form_template, c)

def thank_you(req):
    return direct_to_template(req, 'thank-you.html')

def thank_you_qc(req):
    return direct_to_template(req, 'thank-you-qc.html')

def contact(req):
    if req.method == 'POST':
        procedures = req.POST.getlist('procedures')

        # honeypot
        if req.POST.get('username', None) or req.POST.get('name', None) != "Your full name":
            return redirect(reverse('thank_you'))

        source = req.POST.get('s', None)

        name = "%s %s" % (req.POST.get('first_name', ""), req.POST.get('last_name', ""),)

        if not name.strip():
            return redirect(reverse('thank_you'))

        c = {
            'name' : name, #req.POST.get('first_name'),
            'phone' : req.POST.get('phone_number'),
            'email' : req.POST.get('email'),
            'procedure' : req.POST.get('procedure', ''),
            'procedures' : ", ".join(req.POST.getlist('procedures')),
            'message' : req.POST.get('message'),
            'hear_about_us' : req.POST.get('hear_about_us', ''),
            'address' : req.POST.get('address', ""),
            'location' : req.POST.get("l", ""),
        }

        form_slug = req.GET.get("e")
        form = None

        # append message to existing message if it exists

        try:
            form = Form.objects.get(slug=form_slug)
            if form.message:
                c["message"] = "%s - %s" % (form.message, c["message"],)
        except Form.DoesNotExist:
            pass

        ct = Contact()

        try:
            ct.user = User.objects.get(username='admin')
            ct.updated_by = User.objects.get(username='admin')

            ct.name = name
            ct.phone = c['phone']
            ct.email = c['email']
            ct.message = c['message']
            ct.address = c['address']
            ct.location = req.POST.get("l", "") 
            ct.procedure = c['procedure']
            ct.procedures_long = c['procedures']
            ct.hear_about_us = c['hear_about_us']
            ct.best_call_time = datetime.datetime.now()

            ct.source = source
            ct.save()

            ct.site = [Site.objects.get(pk__exact=settings.SITE_ID)]
        except User.DoesNotExist, Site.DoesNotExist:
            pass

        email_body = render_to_string('email.html', c)

        try:
            site_config = SiteConfig.objects.get(site__pk__exact=settings.SITE_ID)
            emails = Email.objects.filter(site_config=site_config)

            send_mail('[Dr Dayan] New contact', email_body, c['email'], emails.values_list('email_address', flat=True)) 
            
            from django.core.mail import EmailMultiAlternatives

            subject, from_email, to = 'The practice of Steven H. Dayan, MD, FACS thanks you for your contact.', 'MyClinicalTeam@drdayan.com', c["email"]

            text_content = render_to_string("email_response.html", {"name" : name})
            html_content = text_content

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        except SiteConfig.DoesNotExist:
            pass

         
        # show custom thank you message if form is custom
        if form:
            return render(req, "thank_you_message.html", {"message" : form.thank_you_message })

#            if  == "promo3":
#                c["message"] = "Add me to Holiday Card List - " + c["message"] 
#
#    if req.GET.get("e") in ["promo", "promo2"]:
#        return render(req, "promo_message.html") 
#

    if "quick-contact" in source:
        return redirect(reverse('thank_you_qc'))

    return redirect(reverse('thank_you'))

from django.template.loader import render_to_string

def referral(req):
    message = ""

    if req.method == 'POST':

        if req.POST.get('username', None):
            return redirect(reverse('thank_you'))

        source = req.POST.get('s', None)
        if source:
            if source == 'q':
                source = 'quick-contact'
            elif source == 'd':
                source = 'dedicated-contact'
            elif source == 'b':
                source = 'blog-post'
            elif source == 'r':
                source = 'referral'



        c = {
            'name' : req.POST.get('name'),
            'phone' : req.POST.get('phone'),
            'email' : req.POST.get('email'),
            'friends_name' : req.POST.get('friends_name'),
            'friends_email' : req.POST.get('friends_email'),
        }

        ct = Contact()


        try:
            ct.user = User.objects.get(username='admin')
            ct.updated_by = User.objects.get(username='admin')

            ct.name = c['name']
            ct.phone = c['phone']
            ct.email = c['email']
            ct.message = 'Promotion' 
            ct.source = source
            ct.best_call_time = datetime.datetime.now()

            ct.save()

            ct.site = [Site.objects.get(pk__exact=settings.SITE_ID)]
        except User.DoesNotExist, Site.DoesNotExist:
            pass

        ct = Contact()
        try:
            ct.user = User.objects.get(username='admin')
            ct.updated_by = User.objects.get(username='admin')

            ct.name = c['friends_name']
            ct.email = c['friends_email']
            ct.message = 'Promotion' 
            ct.source = source
            ct.best_call_time = datetime.datetime.now()

            ct.save()

            ct.site = [Site.objects.get(pk__exact=settings.SITE_ID)]
        except User.DoesNotExist, Site.DoesNotExist:
            pass

        email_body = render_to_string('promotion_email.html', c)

        try:
            site_config = SiteConfig.objects.get(site__pk__exact=settings.SITE_ID)
            msg = EmailMultiAlternatives('[Dr Dayan] Promotion', email_body, c['email'], [c['friends_email']])
            msg.attach_alternative(email_body, "text/html")
            msg.send()

        except SiteConfig.DoesNotExist:
            pass

        message = render_to_string('embed_message.html',  {'message' : message})

    return HttpResponse(message) #redirect(reverse('thank_you'))


