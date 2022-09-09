from django.contrib import admin
from django.shortcuts import redirect

from django.template.response import TemplateResponse
from django.urls import path

from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
import nested_admin

# Register your models here.
from .models import Database, Parser, SftpConfig, MqttConfig, MqttDeviceType, RawDataStorage, Thing
from .utils import generate_password


def get_db(thing):
    try:
        return Database.objects.get(thing_id=thing.id)
    except Database.DoesNotExist:
        return None


def get_storage(thing):
    try:
        return RawDataStorage.objects.get(thing_id=thing.id)
    except RawDataStorage.DoesNotExist:
        return None


def get_db_string(thing):
    db = get_db(thing)
    if db:
        return 'postgresql://' + db.username + ':' + db.password + '@' + db.url + '/rdm_tsm'
    else:
        return '-'


class ParserInline(nested_admin.NestedStackedInline):
    model = Parser
    extra = 0
    classes = ['collapse']
    fields = ['parser_type', ('delimiter', 'exclude_headlines', 'time_column'), 'timestamp_expression',
              ('start_time', 'end_time')]
    min_num = 1
    validate_min = True
    delimiter = forms.CharField(widget=forms.TextInput(attrs={'size': 1}))
    show_change_link = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(validate_min=self.validate_min, *args, **kwargs)


class MqttConfigInline(nested_admin.NestedStackedInline):
    model = MqttConfig
    fields = ['uri', 'topic', ('username', 'password'), 'device_type']


class SftpConfigInline(nested_admin.NestedStackedInline):
    model = SftpConfig
    inlines = [ParserInline]
    fields = ['uri', ('username', 'password'), 'filename_pattern']


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = '__all__'


class ThingAdmin(nested_admin.NestedModelAdmin):
    model = Thing
    inlines = [SftpConfigInline, MqttConfigInline]
    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', get_db_string, 'group_id', 'datasource_type', 'isActivated', ),
        }),
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'group_id', 'datasource_type', 'isActivated')
    get_db_string.short_description = 'DB-Connection'
    list_filter = ('datasource_type', 'group_id', )
#    list_editable = ('isActivated',)

    def get_readonly_fields(self, request, obj):
        fields = ['thing_id', get_db_string, ]
        if obj.isActivated:
            fields.append('isActivated')
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        users_groups = request.user.groups.all()
        if request.user.is_superuser:
            return qs
        return qs.filter(group_id__in=users_groups)

    class Media:
        js = ('thing_form.js',)


@receiver(post_save, sender=Thing)
def create_database(sender, instance, **kwargs):
    thing = instance

    if get_db(instance) is None:
        database = Database()
        database.url = 'postgres.intranet.ufz.de:5432'
        database.username = thing.group_id.name + '_' + str(thing.thing_id)
        database.password = generate_password(40)
        database.thing = thing
        database.save()


@receiver(post_save, sender=Thing)
def create_raw_data_storage(sender, instance, **kwargs):
    thing = instance

    if get_storage(instance) is None:
        database = RawDataStorage()
        database.bucket = thing.group_id.name + '123456'
        database.access_key = thing.group_id.name + '_' + str(thing.thing_id)
        database.secret_key = generate_password(40)
        database.thing = thing
        database.save()


class BasicAdminSite(admin.AdminSite):
    def about(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.each_context(request),
        )
        return TemplateResponse(request, "admin/about.html", context)

    def redirect_basic_users_on_index_page(self, request):
        if request.user.is_superuser:
            return admin.site.index(request)
        return redirect('admin:tsm_thing_changelist')

    def redirect_basic_users_on_main_page(self, request):
        if request.user.is_superuser:
            return admin.site.app_index(request, 'tsm')
        return redirect('admin:tsm_thing_changelist')


basic_site = BasicAdminSite()
basic_site.register(Thing, ThingAdmin)
basic_site.enable_nav_sidebar = False

admin.site.register(Thing, ThingAdmin)
admin.site.register(MqttDeviceType)
admin.site.enable_nav_sidebar = False
