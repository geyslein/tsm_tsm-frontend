from django.contrib import admin

from django.shortcuts import redirect
from django.urls import path
from django.template.response import TemplateResponse

from django.db.models.signals import post_save
from django.dispatch import receiver

# Register your models here.
from .models import Database, MqttDeviceType, RawDataStorage, Thing
from .utils import get_db, get_storage, generate_password, start_ingest
from .forms import ThingAdmin


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
def add_related_entities(sender, instance, **kwargs):
    thing = instance
    if get_db(thing) is None:
        database = Database()
        database.url = 'postgres.intranet.ufz.de:5432'
        database.username = thing.group_id.name + '_' + str(thing.thing_id)
        database.password = generate_password(40)
        database.thing = thing
        database.save()

    if get_storage(thing) is None:
        name = thing.group_id.name + '_' + str(thing.thing_id)

        database = RawDataStorage()
        database.bucket = name
        database.access_key = name
        database.secret_key = generate_password(40)
        database.thing = thing
        database.save()

    if thing.is_ready and thing.is_active is False:
        start_ingest(thing)
