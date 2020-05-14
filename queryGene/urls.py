from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from .views import GenesAssociated,GenesAssociatedGET,queryExpression,queryPlotPromoter

urlpatterns = [
    url(r'^ajax_gtex$', queryExpression, name='ajax_gtex'),
    url(r'^ajax_promoter$', queryPlotPromoter, name='ajax_promoter'),
    url(r'^gene/(?P<gene>[\w-]+)', GenesAssociatedGET.as_view()),
    url('', GenesAssociated.as_view(), name='queryGene'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)