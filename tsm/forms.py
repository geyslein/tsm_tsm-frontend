from django.contrib import admin

from .models import Parser, MqttDeviceType, RawDataStorage, Thing
from django.contrib.auth.models import Group
from .utils import get_connection_string

from django import forms
from django.core.exceptions import ValidationError


class ParserInlineFormset(forms.BaseInlineFormSet):
    model = Parser

    def clean(self):
        if self.instance.datasource_type == 'SFTP':
            count_active_parser = 0
            for form in self.forms:
                cleaned_data = form.clean()

                if cleaned_data == {}:
                    continue    # form is empty and will not be saved. Skip validation.

                for field in ['delimiter', 'timestamp_column', 'timestamp_format', ]:
                    if not cleaned_data[field]:
                        form.add_error(field, 'This field could not be empty.')

                if not cleaned_data.get('DELETE', False):
                    if cleaned_data['is_active']:
                        count_active_parser += 1

            if count_active_parser == 0:
                raise ValidationError("A thing with SFTP-Settings must have one active parser.")

            if count_active_parser > 1:
                raise ValidationError("A thing could only have one active parser.")


class ParserInline(admin.StackedInline):
    model = Parser
    formset = ParserInlineFormset
    classes = ['collapse']
    fields = [('type', 'delimiter'), ('exclude_headlines', 'exclude_footlines'), ('timestamp_column', 'timestamp_format'),
              ('is_active'), ]
    min_num = 1
    extra = 0
    delimiter = forms.CharField(widget=forms.TextInput(attrs={'size': 1}))


class ThingForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))

    class Meta:
        model = Thing
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        fields = []
        if cleaned_data.get("datasource_type") == 'SFTP':
            fields = ['sftp_uri', 'sftp_username', 'sftp_password', 'sftp_filename_pattern', ]

        if cleaned_data.get("datasource_type") == 'MQTT':
            fields = ['mqtt_uri', 'mqtt_username', 'mqtt_password', 'mqtt_topic', 'mqtt_device_type', ]

        print(cleaned_data)

        for field in fields:
            if cleaned_data.get(field):
                continue
            self.add_error(field, 'This field could not be empty.')


class ProjectFilter(admin.SimpleListFilter):
    title = 'Projects'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        result = []

        if request.user.is_superuser:
            groups = Group.objects.all()
        else:
            groups = request.user.groups.all()

        for group in groups:
            result.append((group.id, group.name))
        return result

    def queryset(self, request, query_set):
        if self.value():
            return query_set.filter(group__id=self.value())
        else:
            return query_set


class ThingAdmin(admin.ModelAdmin):
    inlines = [ParserInline]
    fieldsets = [
        (None, {
            'fields': ('name', 'group', 'description', 'thing_id', get_connection_string, 'datasource_type', 'is_ready',),
        }),
        ('SFTP-Settings', {
            'fields': ('sftp_uri', ('sftp_username', 'sftp_password'), 'sftp_filename_pattern', ),
            'classes': ('sftp-settings',),
        }),
        ('MQTT-Settings', {
            'fields': (('mqtt_uri', 'mqtt_topic'), ('mqtt_username', 'mqtt_password'), 'mqtt_device_type', ),
            'classes': ('mqtt-settings',),
        })
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'group', 'datasource_type', 'is_ready')
    list_filter = ('datasource_type', ProjectFilter,)
    get_connection_string.short_description = 'DB-Connection'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if not superuser, a user can only select things from his groups (=projects)
        if not request.user.is_superuser:
            if db_field.name == "group":
                kwargs["queryset"] = Group.objects.filter(id__in=request.user.groups.all())

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj):
        fields = ['thing_id', get_connection_string, 'is_created']
        if obj is not None and obj.is_ready:
            fields.append('is_ready')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # if not superuser, a user can see only things from his groups (=projects)
        users_groups = request.user.groups.all()
        if request.user.is_superuser:
            return qs
        return qs.filter(group__in=users_groups)

    class Media:
        js = ('thing_form.js',)
