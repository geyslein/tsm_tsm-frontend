from django.contrib import admin

# Register your models here.

from .models import Parser, Thing, SftpConfig, MqttConfig


class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']


class SftpConfigInline(admin.StackedInline):
    model = SftpConfig
    classes = ['collapse']


class MqttConfigInline(admin.StackedInline):
    model = MqttConfig
    classes = ['collapse']


class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [SftpConfigInline, MqttConfigInline, ParserInline]

    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', 'project', 'datasource_type',),
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
