from django.contrib import admin
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
import nested_admin

# Register your models here.
from .models import Database, Parser, SftpConfig, MqttConfig, Thing


def get_db(thing):
    try:
        return Database.objects.get(thing_id=thing.id)
    except Database.DoesNotExist:
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
    fields = ['parser_type', ('delimiter', 'exclude_headlines', 'time_column'), 'timestamp_expression', ('start_time', 'end_time')]
    min_num = 1
    validate_min = True
    delimiter = forms.CharField(label='sdsd', widget=forms.TextInput(attrs={'size': 1 }))
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
        fields = ('__all__')


class ThingAdmin(nested_admin.NestedModelAdmin):
    model = Thing
    inlines = [SftpConfigInline, MqttConfigInline]
    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', get_db_string, 'project', 'datasource_type',),
        }),
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'project', 'datasource_type')
    get_db_string.short_description = 'DB-Connection'

    def get_readonly_fields(self, request, obj):
        return ['thing_id', get_db_string,]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(userid=request.user)

    def save_model(self, request, obj, form, change):

        # create Minio-Credentials
        # create JSON for dispatcher

        if not request.user.is_superuser:
            obj.userid = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('thing_form.js',)


admin.site.register(Thing, ThingAdmin)


@receiver(post_save, sender=Thing)
def create_database(sender, instance, **kwargs):
    thing = instance

    if get_db(instance) is None:
        database = Database()
        database.url = 'postgres.intranet.ufz.de:5432'
        database.username = thing.project + '_' + str(thing.thing_id)
        database.password = '123456'    # TODO
        database.thing = thing
        database.save()
