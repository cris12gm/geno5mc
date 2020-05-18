from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import RegionAssociated, queryViewMore, queryPlotMeth

urlpatterns = [
    url(r'^ajax_regionViewMore$', queryViewMore, name='ajax_regionViewMore'),
    url(r'^ajax_ButtonRegion$', queryPlotMeth, name='ajax_ButtonRegion'),
    url('', RegionAssociated.as_view(), name='queryRegion'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)