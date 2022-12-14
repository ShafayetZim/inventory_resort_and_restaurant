from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('brand', views.brand, name='brand-page'),
    path('manage_brand', views.manage_brand, name='manage-brand'),
    path('manage_brand/<int:pk>', views.manage_brand, name='manage-brand-pk'),
    path('save_brand', views.save_brand, name='save-brand'),
    path('delete_brand/<int:pk>', views.delete_brand, name='delete-brand'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
