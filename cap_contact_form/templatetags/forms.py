from django import template
from models import ContactForm

register = template.Library()


@register.assignment_tag
def render_form(slug=None):
    contact_form = ContactForm.objects.get(slug=slug)
    return contact_form

