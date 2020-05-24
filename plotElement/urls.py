from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import plotElements,plotElementsTour,downloadMethData


urlpatterns = [
    url(r'^tour/', plotElementsTour.as_view(), name='plotElement_Tour'),
    url('',plotElements.as_view(), name='plotElement'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
