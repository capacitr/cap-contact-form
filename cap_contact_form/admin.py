from django.contrib import admin

from models import Contact
from models import Form

class ContactAdmin(admin.ModelAdmin):
    #actions = [export_as_csv_action()]

    def show_procedures(obj):
        return "%s%s" % (obj.procedure, obj.procedures_long,)

    list_display = ['date_created', 'name', 'phone', 'email', 'message', 'source', 'location']

class ContactFormAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ContactForm, ContactFormAdmin)

