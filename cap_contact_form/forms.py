from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200)
    from_email = forms.EmailField(max_length=200)
    message = forms.CharField(max_length=500)

