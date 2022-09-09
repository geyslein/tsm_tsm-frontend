"""dqvm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.auth.models import User

from django.contrib import admin
from main.admin import basic_site
from main.models import Thing, Parser
from rest_framework import routers, serializers, viewsets

from django.conf import settings
from django.conf.urls.static import static


class ParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parser
        fields = '__all__'


class ThingSerializer(serializers.HyperlinkedModelSerializer):
    #parser = ParserSerializer(many=True)
    class Meta:
        model = Thing
        fields = ['name', 'thing_id', 'project']


class ThingViewSet(viewsets.ModelViewSet):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer


router = routers.DefaultRouter()
router.register(r'things', ThingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tsm/', basic_site.admin_view(basic_site.redirect_basic_users_on_index_page)),
    path('tsm/main/', basic_site.admin_view(basic_site.redirect_basic_users_on_main_page)),
    path('tsm/about/', basic_site.admin_view(basic_site.about), name='about'),
    path('tsm/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
