from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

# Register your models here.

from .models import Parser, Thing, SftpConfig, MqttConfig


class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']


class SftpConfigInlineFormSet(BaseInlineFormSet):
    def clean(self):
        if self.instance.datasource_type == 'SFTP':
            return


class SftpConfigInline(admin.StackedInline):
    model = SftpConfig
    formset = SftpConfigInlineFormSet
    classes = ['collapse']


class MqttConfigInline(admin.StackedInline):
    model = MqttConfig
    classes = ['collapse']


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ('__all__')

    def clean(self):
        raise ValidationError(self.cleaned_data)

class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [SftpConfigInline, MqttConfigInline, ParserInline]

    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', 'database', 'project', 'datasource_type',),
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
