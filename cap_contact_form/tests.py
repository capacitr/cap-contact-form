"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from dbtemplates.models import Template
from models import ContactForm, Source, Contact
from django.utils import simplejson

class TestContactForm(TestCase):
    fixtures = [
        'test_data.yaml'
        ]

    def test_form_template(self):
        template_params =  {
                'name' : 'page12.html',
                'content' : 'test'
            }

        template = Template(**template_params)
        template.save()

        source_params = {
                'source' : 'test-source',
                'slug' : 'test-source'
                }

        source = Source(**source_params)
        source.save()

        form_params = {
            'name' : 'test',
            'slug' : 'test',
            'template' : template,
            'message' : 'test1',
            'thank_you_message' : 'thank_you',
            'form_type' : source,
            'height' : '100',
            'width' : '200'
            }

        form = ContactForm(**form_params)

        embed_code = """<iframe style="border: none; 
        overflow: hidden;" src="page12.html" frameborder="0" 
        scrolling="no" width="200" height="100"></iframe>"""

        assert form.embed_code == embed_code, True

    def test_contact_attributes_from_fixtures(self):
        contact = Contact.objects.get(name="test")
        assert contact.get_attribute("test1") == "test", True

    def test_contact_attributes(self):
        attributes = {
                'procedure' : 'test',
                'procedures_long' : 'long',
                'contact_by' : 'June 12',
                'best_call_time' : '12am',
                'hear_about_us' : 'magazine',
                'date_contacted' : 'july 1',
                'call_message' : 'hey there',
                'location' : 'none'
            }

        contact_params = {
                'name' : 'test',
                'address' : '123 fake st.',
                'city' : 'test city',
                'state' : 'state',
                'zip_code' : 'zip_code',
                'phone' : 'phone',
                'email' : 'email',
                'message' : 'test',
                'attributes' : simplejson.dumps(attributes)
                }

        contact = Contact(**contact_params)
        contact.save()


        assert contact.json_attributes == attributes, True

        assert contact.get_attribute("procedure") == "test", True
        assert contact.get_attribute("procedures_long") == "long", True

    def test_source(self):
        source = Source.objects.get(slug="test")

