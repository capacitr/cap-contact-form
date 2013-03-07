from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    #actions = [export_as_csv_action()]

    def show_procedures(obj):
        return "%s%s" % (obj.procedure, obj.procedures_long,)

    list_display = ['date_created', 'name', 'phone', 'email', 'message', 'source', 'location']

