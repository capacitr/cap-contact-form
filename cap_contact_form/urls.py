from django.conf.urls.defaults import patterns, include, url
from views import ContactUsView


urlpatterns = patterns('',
    url(r'^$', ContactUsView.as_view(),  name='contact_us'),
)

