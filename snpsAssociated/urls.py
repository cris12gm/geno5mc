from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from snpsAssociated import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^querySNP/', include('querySNP.urls')),
    url(r'^queryGene/', include ('queryGene.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
