from django.db import models

from django.utils import simplejson

CONTACT_BY = (
    ('email', 'email'),
    ('phone', 'phone')
    )

SOURCE_CHOICES = (
    ('quick-contact', 'quick-contact'),
    ('dedicated-contact', 'dedicated-contact'),
    ('blog-post', 'blog-post'),
    ('referral', 'referral')
    )

FORM_TEMPLATES = (
    ("embed_basic.html", "Basic Contact Form"),
    ("embed_promo_holiday.html", "Trivia Form"),
)

class Source(models.Model):
    source = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __unicode__(self):
        return self.source

class Contact(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    address = models.TextField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)

    email = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    source = models.CharField(max_length=255, choices=SOURCE_CHOICES, blank=True, default="dedicated-contact")

#    procedure = models.CharField(max_length=255)
#    procedures_long = models.CharField(max_length=255, blank=True, null=True)
#
#    contact_by = models.CharField(max_length=255, choices=CONTACT_BY)
#    best_call_time = models.DateTimeField(blank=True)
#    hear_about_us = models.CharField(max_length=255, default="", blank=True)
#    message = models.TextField()
#
#    date_contacted = models.DateTimeField(null=True, blank=True)
#    call_message = models.TextField(blank=True)
#    source = models.CharField(max_length=255, choices=SOURCE_CHOICES, blank=True, default="dedicated-contact")
#
#    location = models.CharField(max_length=255, blank=True)

    attributes = models.TextField(blank=True)

    @property
    def json_attributes(self):
        return simplejson.loads(self.attributes)

    def get_attribute(self, val):
        attributes = self.json_attributes
        return attributes.get(val, None)

class Email(models.Model):
    email = models.EmailField(max_length=255)

    def __unicode__(self):
        return self.email

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    template = models.ForeignKey("dbtemplates.Template")
    to = models.ManyToManyField(Email)

    message = models.TextField(max_length=255, blank=True, default="")
    thank_you_message = models.TextField(blank=True)
    form_type = models.ForeignKey("Source")

    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)

    @property
    def embed_code(self):
        url, height, width = self.template.name, self.height, self.width
        code = """<iframe style="border: none; 
        overflow: hidden;" src="%s" frameborder="0" 
        scrolling="no" width="%s" height="%s"></iframe>""" % (url, width, height)
        return code 

    def __unicode__(self):
        return "%s" % self.name

