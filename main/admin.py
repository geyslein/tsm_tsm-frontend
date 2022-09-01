from django.contrib import admin

# Register your models here.

from .models import SftpSettings, MqttSettings, ParserType, Parser, Database, Datasource, Thing


class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']


class SftpSettingsInline(admin.StackedInline):
    model = SftpSettings


class MqttSettingsInline(admin.StackedInline):
    model = MqttSettings


class DatasourceAdmin(admin.ModelAdmin):
    model = Datasource
    inlines = [SftpSettingsInline, MqttSettingsInline]

    class Media:
        js = ('shuttle_form.js',)


class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [ParserInline]


admin.site.register(Datasource, DatasourceAdmin)
admin.site.register(Database)
admin.site.register(Parser)
admin.site.register(Thing, ThingAdmin)
admin.site.register(ParserType)
