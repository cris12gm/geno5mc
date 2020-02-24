from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import SNPAssociated,SNPAssociatedGET,SNPAssociatedTour,queryGeneDescription,queryEnhancerDescription


urlpatterns = [
    url(r'^ajax_gene$', queryGeneDescription, name='ajax_gene'),
    url(r'^ajax_enhancer$', queryEnhancerDescription, name='ajax_enhancer'),
    url(r'^tour', SNPAssociatedTour.as_view(), name='querySNP_Tour'),
    url(r'^snp/(?P<snp>[\w-]+)', SNPAssociatedGET.as_view()),
    url('', SNPAssociated.as_view(), name='querySNP'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
