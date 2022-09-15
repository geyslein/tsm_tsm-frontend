from django.contrib import admin

from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse

from django.db.models.signals import post_save
from django.dispatch import receiver

# Register your models here.
from .models import Database, MqttDeviceType, RawDataStorage, Thing
from .utils import create_db_username, get_db, get_storage, get_random_chars, start_ingest, update_parser_properties_of_thing_in_tsm_db
from .forms import ThingAdmin
import os
import time


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
    database = get_db(thing)

    if database is None:
        database = Database()
        database.url = os.environ.get('TSM_DATABASE_HOST')
        database.name = os.environ.get('TSM_DATABASE_NAME')
        database.username = create_db_username(thing)
        database.password = get_random_chars(24)
        database.thing = thing
        database.save()

    if get_storage(thing) is None:

        name = 'ufz_' + str(thing.thing_id) # TODO avoid more than 63 chars but make it more readable

        storage = RawDataStorage()
        storage.bucket = name
        storage.access_key = name
        storage.secret_key = get_random_chars(40)
        storage.thing = thing
        storage.save()

    if os.environ.get('SETUP_DB_AND_STORAGE'):
        if thing.is_active and database:
            if database.is_created:
                update_parser_properties_of_thing_in_tsm_db(thing)

        if database and thing.is_ready and thing.is_active is False:
            if not database.is_created:
                start_ingest(thing, database)

                # wait for dispatcher creating database.
                # Otherwise this function will be called too early again (because of saving 'thing')
                # ('update_parser_properties_of_thing_in_tsm_db' would be called before database exists
                time.sleep(2)

                thing.is_active = True
                thing.save()
