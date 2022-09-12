
from .models import Parser, SftpConfig, MqttConfig, MqttDeviceType, RawDataStorage, Thing
from .utils import get_db_string

import nested_admin
from django import forms
from django.core.exceptions import ValidationError


class ParserInlineFormset(nested_admin.NestedInlineFormSet):
    model = Parser

    def clean(self):
        super().clean()
        if self.instance.thing.datasource_type == 'SFTP':
            count = 0
            for form in self.forms:
                if form.is_valid():
                    if form.cleaned_data == {}:
                        continue
                    count += 1
            if count < 1:
                raise ValidationError('Please enter at least one Parser.')


class ParserInline(nested_admin.NestedStackedInline):
    model = Parser
    formset = ParserInlineFormset
    classes = ['collapse']
    fields = [('type', 'delimiter'), ('exclude_headlines', 'exclude_footlines'), ('timestamp_column', 'timestamp_format'),
              ('start_time', 'end_time')]
    min_num = 1
    extra = 0
    delimiter = forms.CharField(widget=forms.TextInput(attrs={'size': 1}))


class MqttInlineFormset(nested_admin.NestedInlineFormSet):
    model = MqttConfig

    def clean(self):
        if self.instance.datasource_type == 'MQTT' and self.cleaned_data == [{}]:
            raise ValidationError('Please enter MQTT settings.')


class SftpInlineFormset(nested_admin.NestedInlineFormSet):
    model = SftpConfig

    def clean(self):
        if self.instance.datasource_type == 'SFTP' and self.cleaned_data == [{}]:
            raise ValidationError('Please enter SFTP settings.')


class MqttConfigInline(nested_admin.NestedStackedInline):
    model = MqttConfig
    can_delete = False
    formset = MqttInlineFormset
    fields = ['uri', 'topic', ('username', 'password'), 'device_type']

    def clean(self):
        if self.instance.datasource_type == 'MQTT':
            self.add_error('test')


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
            'fields': ('name', 'thing_id', get_db_string, 'group_id', 'datasource_type', ('is_ready', 'is_active'),),
        }),
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'group_id', 'datasource_type', 'is_ready', 'is_active')
    list_filter = ('datasource_type', 'group_id',)
    get_db_string.short_description = 'DB-Connection'

    def get_readonly_fields(self, request, obj):
        fields = ['thing_id', get_db_string, 'is_active']
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