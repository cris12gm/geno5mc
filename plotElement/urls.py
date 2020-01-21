from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import plotEnhancers,plotEnhancers2


urlpatterns = [
    url('',plotEnhancers.as_view(), name='plotElement'),
    url(r'^test/', plotEnhancers2.as_view()),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
