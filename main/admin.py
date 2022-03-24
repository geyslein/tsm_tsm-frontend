from django.contrib import admin

# Register your models here.

from .models import Shuttle, SftpSettings, MqttSettings, RawdataStorage, ParserType, Parser, DatastoreType, Datastore, Datasource


class SftpSettingsInline(admin.TabularInline):
    model = SftpSettings


class MqttSettingsInline(admin.TabularInline):
    model = MqttSettings


class ShuttleAdmin(admin.ModelAdmin):
    model = Shuttle
    inlines = [SftpSettingsInline, MqttSettingsInline]

    class Media:
        js = ('shuttle_form.js',)


admin.site.register(Shuttle, ShuttleAdmin)
admin.site.register(Datasource)
admin.site.register(DatastoreType)
admin.site.register(Datastore)
admin.site.register(Parser)
admin.site.register(ParserType)
