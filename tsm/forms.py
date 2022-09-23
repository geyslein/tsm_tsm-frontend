
from .models import Parser, SftpConfig, MqttConfig, MqttDeviceType, RawDataStorage, Thing
from .utils import get_connection_string

import nested_admin
from django import forms
from django.core.exceptions import ValidationError
from .validation import check_parser_time_ranges, validate_single_parser, get_number_of_valid_forms, check_required_fields


class ParserInlineFormset(nested_admin.NestedInlineFormSet):
    model = Parser

    def clean(self):
        if not hasattr(self.instance, 'thing'):
            return

        if self.instance.thing.datasource_type == 'SFTP':
            #check_required_fields(self.forms, ['delimiter', 'timestamp_column', 'timestamp_format', ])

            #validate_single_parser(self.forms)

            #check_parser_time_ranges(self.forms)

            count = get_number_of_valid_forms(self.forms)
            if count < 1:
                raise ValidationError('Please enter at least one Parser.')


class ParserInline(nested_admin.NestedStackedInline):
    model = Parser
    formset = ParserInlineFormset
    classes = ['collapse']
    fields = [('type', 'delimiter'), ('exclude_headlines', 'exclude_footlines'), ('timestamp_column', 'timestamp_format'),
              ('start_time', 'end_time'), ]
    min_num = 1
    extra = 0
    delimiter = forms.CharField(widget=forms.TextInput(attrs={'size': 1}))


class MqttInlineFormset(nested_admin.NestedInlineFormSet):
    model = MqttConfig

    def clean(self):
        if self.instance.datasource_type == 'MQTT':
            check_required_fields(self.forms, ['uri', 'username', 'password', 'topic', ])


class SftpInlineFormset(nested_admin.NestedInlineFormSet):
    model = SftpConfig

    def clean(self):
        if self.instance.datasource_type == 'SFTP':
            check_required_fields(self.forms, ['uri', 'username', 'password', 'filename_pattern', ])


class MqttConfigInline(nested_admin.NestedStackedInline):
    model = MqttConfig
    can_delete = False
    formset = MqttInlineFormset
    fields = ['uri', 'topic', ('username', 'password'), 'device_type']


class SftpConfigInline(nested_admin.NestedStackedInline):
    model = SftpConfig
    can_delete = False
    formset = SftpInlineFormset
    fields = ['uri', ('username', 'password'), 'filename_pattern']
    inlines = [ParserInline]


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = '__all__'


class ThingAdmin(nested_admin.NestedModelAdmin):
    inlines = [SftpConfigInline, MqttConfigInline]
    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', get_connection_string, 'group_id', 'datasource_type', ('is_ready', 'is_active'),),
        }),
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'group_id', 'datasource_type', 'is_ready', 'is_active')
    list_filter = ('datasource_type', 'group_id',)
    get_connection_string.short_description = 'DB-Connection'

    def get_readonly_fields(self, request, obj):
        fields = ['thing_id', get_connection_string, 'is_active']
        if obj is not None and obj.is_ready:
            fields.append('is_ready')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        users_groups = request.user.groups.all()
        if request.user.is_superuser:
            return qs
        return qs.filter(group_id__in=users_groups)

    class Media:
        js = ('thing_form.js',)
