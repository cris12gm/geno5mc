from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import SNPAssociated,SNPAssociatedGET,SNPAssociatedTour,SNPAssociatedTourPOST


urlpatterns = [
    url(r'^tour', SNPAssociatedTour.as_view(), name='querySNP_Tour'),
    url(r'^2tour', SNPAssociatedTourPOST.as_view(), name='querySNP_Tour_2'),
    url(r'^snp/(?P<snp>[\w-]+)', SNPAssociatedGET.as_view()),
    url('', SNPAssociated.as_view(), name='querySNP'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
