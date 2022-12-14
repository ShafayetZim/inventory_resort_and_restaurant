from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
