from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import SNPAssociated,SNPAssociatedGET


urlpatterns = [
    url(r'^snp/(?P<snp>[\w-]+)', SNPAssociatedGET.as_view()),
    url('', SNPAssociated.as_view(), name='querySNP'),
    url(r'^snp/[A-za-z0-9]+', SNPAssociatedGET.as_view()),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
