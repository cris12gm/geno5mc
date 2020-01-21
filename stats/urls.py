from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import stats


urlpatterns = [
    url('',stats.as_view(), name='stats'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
