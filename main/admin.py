from django.contrib import admin

# Register your models here.

from .models import Parser, Thing


class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']


class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [ParserInline]

    fieldsets = [
        (None, {
            'fields': ('name','thing_id','project','database','datasource_type',),
        }),
        ('SFTP-Settings', {
            'fields': ('sftp_uri', 'sftp_username', 'sftp_password', 'sftp_filename_pattern',),
            'classes': ('collapse', 'sftp-settings',),
        }),
        ('MQTT-Settings', {
            'fields': ('mqtt_uri', 'mqtt_username', 'mqtt_password', 'mqtt_topic',),
            'classes': ('collapse', 'mqtt-settings',),
        })
    ]

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
