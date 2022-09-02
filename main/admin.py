from django.contrib import admin
from django import forms

# Register your models here.
from .models import Parser, Thing


sftp_fields = ['sftp_uri','sftp_username','sftp_password','sftp_filename_pattern',]
mqtt_fields = ['mqtt_uri','mqtt_username','mqtt_password','mqtt_topic',]

class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ('__all__')

    def clean(self):
        form_data = self.cleaned_data
        configs = [('SFTP', sftp_fields), ('MQTT', mqtt_fields)]

        for (type, fields) in configs:
            if form_data['datasource_type'] == type:
                for field in fields:
                    if form_data[field] is None or form_data[field] == '':
                        self.add_error(field, 'This field could not be empty.')


class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [ParserInline]

    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', 'database', 'project', 'datasource_type',),
        }),
        ('SFTP-Settings', {
            'fields': sftp_fields,
            'classes': ('collapse', 'sftp-config',),
        }),
        ('MQTT-Settings', {
            'fields': mqtt_fields,
            'classes': ('collapse', 'mqtt-config',),
        })
    ]
    form = ThingForm

    def get_readonly_fields(self, request, obj):
        return ['thing_id', 'database',]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(userid=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.userid = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('thing_form.js',)


admin.site.register(Thing, ThingAdmin)
