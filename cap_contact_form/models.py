from django.db import models

SOURCE_CHOICES = (
    ('quick-contact', 'quick-contact'),
    ('dedicated-contact', 'dedicated-contact'),
    ('blog-post', 'blog-post'),
    ('referral', 'referral')
    )

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
#

class Attribute(models.Model):
    post = models.ForeignKey('cap_contact_form.Contact')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('post', 'slug')


FORM_TEMPLATES = (
    ("embed_basic.html", "Basic Contact Form"),
    ("embed_promo_holiday.html", "Trivia Form"),
)

class Form(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    form_template = models.CharField(max_length=255, choices=FORM_TEMPLATES)

    message = models.TextField(max_length=255, blank=True, default="")
    thank_you_message = models.TextField(blank=True)
    form_type = models.CharField(max_length=255, choices=SOURCE_CHOICES, default="blog-post")

    @property
    def embed_code(self):
        code = ""
        try:
            sizes = {
                "embed_basic.html" : (740, 250),
                "embed_promo_holiday.html" : (740, 250),
            }
            code = """<iframe style="border: none; overflow: hidden;" src="http://www.drdayan.com%s" frameborder="0" scrolling="no" width="%s" height="%s"></iframe>""" % (self.get_absolute_url(), sizes[self.form_template][0], sizes[self.form_template][1])
        except KeyError:
            pass

        return code 

    def __unicode__(self):
        return "%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ("drdayan.views.get_form", (), {
            "form_slug" : self.slug 
        })

