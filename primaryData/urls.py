from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import primaryData


urlpatterns = [
    url('',primaryData.as_view(), name='primaryData'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
