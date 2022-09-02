from django.contrib import admin
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver


# Register your models here.
from .models import Database, Parser, Thing


sftp_fields = ['sftp_uri','sftp_username','sftp_password','sftp_filename_pattern',]
mqtt_fields = ['mqtt_uri','mqtt_username','mqtt_password','mqtt_topic',]


def get_db_if_exists(thing):
    try:
        return Database.objects.get(thing_id=thing.id)
    except Database.DoesNotExist:
        return None


def get_db_string_if_exists(thing):
    db = get_db_if_exists(thing)
    if db:
        return 'postgresql://' + db.username + ':' + db.password + '@' + db.url + '/rdm_tsm'
    else:
        return '-'


class ParserInline(admin.StackedInline):
    model = Parser
    extra = 1
    classes = ['collapse']
    fields = ['parser_type', 'delimiter', 'exclude_headlines', ('time_column', 'timestamp_expression'), ('start_time', 'end_time')]


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ('__all__')

    def clean(self):
        form_data = self.cleaned_data
        configs = [('SFTP', sftp_fields), ('MQTT', mqtt_fields)]

        for (type, fields) in configs:
            if form_data['datasource_type'] == type:
                for field in fields:
                    if form_data[field] is None or form_data[field] == '':
                        self.add_error(field, 'This field could not be empty.')


class ThingAdmin(admin.ModelAdmin):
    model = Thing
    inlines = [ParserInline]

    fieldsets = [
        (None, {
            'fields': ('name', 'thing_id', get_db_string_if_exists, 'project', 'datasource_type',),
        }),
        ('SFTP-Settings', {
            'fields': sftp_fields,
            'classes': ('collapse', 'sftp-config',),
        }),
        ('MQTT-Settings', {
            'fields': mqtt_fields,
            'classes': ('collapse', 'mqtt-config',),
        })
    ]
    form = ThingForm
    list_display = ('name', 'thing_id', 'project', 'datasource_type')

    def get_readonly_fields(self, request, obj):
        return ['thing_id', get_db_string_if_exists,]

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

    if get_db_if_exists(instance) is None:
        database = Database()
        database.url = 'postgres.intranet.ufz.de:5432'
        database.username = thing.project + '_' + str(thing.thing_id)
        database.password = '123456'    # TODO
        database.thing = thing
        database.save()
