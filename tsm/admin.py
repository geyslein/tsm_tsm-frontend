from django.contrib import admin
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Database, MqttDeviceType, Parser, RawDataStorage, Thing

from .utils import create_db_username, create_bucket_name, get_db_by_thing, get_storage_by_thing, get_random_chars, get_json_config
from .mqtt_actions import publish_thing_config
from .forms import ThingAdmin
import os

CREATEDB_POSTGRES_HOST = os.environ.get('CREATEDB_POSTGRES_HOST')
CREATEDB_POSTGRES_DATABASE = os.environ.get('CREATEDB_POSTGRES_DATABASE')


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


@receiver(post_save, sender=Thing)
def process_thing(sender, instance, **kwargs):
    thing = instance
    database = get_db_by_thing(thing)

    if database is None:
        database = Database()
        database.url = "postgres.intranet.ufz.de"
        database.name = "rdm_tsm?sslmode=verify-full"
        database.username = create_db_username(thing.group)
        database.password = get_random_chars(24)
        database.group = thing.group
        database.save()

    if get_storage_by_thing(thing) is None:

        name = create_bucket_name(thing)

        storage = RawDataStorage()
        storage.bucket = name
        storage.access_key = name
        storage.secret_key = get_random_chars(40)
        storage.thing = thing
        storage.save()

    if thing.datasource_type == 'MQTT':
        publish(thing)


@receiver(post_save, sender=Parser)
def publish_settings(sender, instance, **kwargs):
    publish(instance.thing)


def publish(thing):
    if thing.is_ready:
        # create or update thing in the respective database
        publish_thing_config(get_json_config(thing))


@receiver(pre_save, sender=Thing)
def add_mqtt_password_hash(sender, instance, **kwargs):
    thing = instance
    thing.mqtt_hashed_password = make_password(
        thing.mqtt_password, hasher='PBKDF2')
