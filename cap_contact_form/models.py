from django.db import models

from django.utils import simplejson

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

    source = models.ForeignKey("Source") 

    attributes = models.TextField(blank=True)

    @property
    def json_attributes(self):
        return simplejson.loads(self.attributes)

    def get_attribute(self, name):
        attributes = self.json_attributes
        return attributes.get(name, None)

class AdminEmail(models.Model):
    email = models.EmailField(max_length=255)

    def __unicode__(self):
        return self.email

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    template = models.ForeignKey("dbtemplates.Template")
    submission_template = models.ForeignKey("dbtemplates.Template")
    email_template = models.ForeignKey("dbtemplates.Template")
    email_subject_line = models.CharField(max_length=255)

    to = models.ManyToManyField("AdminEmail")

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

