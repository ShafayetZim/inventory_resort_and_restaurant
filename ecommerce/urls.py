from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
#     path('brand',views.brand,name='brand-page'),
#     path('manage_brand',views.manage_brand,name='manage-brand'),
#     path('manage_brand/<int:pk>',views.manage_brand,name='manage-brand-pk'),
#     path('view_brand/<int:pk>',views.view_brand,name='view-brand-pk'),
#     path('save_brand',views.save_brand,name='save-brand'),
#     path('delete_brand/<int:pk>',views.delete_brand,name='delete-brand'),
#     path('products',views.products,name='product-page'),
#     path('manage_product',views.manage_product,name='manage-product'),
#     path('manage_product/<int:pk>',views.manage_product,name='manage-product-pk'),
#     path('view_product',views.view_product,name='view-product'),
#     path('view_product/<int:pk>',views.view_product,name='view-product-pk'),
#     path('save_product',views.save_product,name='save-product'),
#     path('delete_product/<int:pk>',views.delete_product,name='delete-product'),
#
# path('purchase',views.purchase,name='purchase-page'),
#     path('manage_purchase',views.manage_purchase,name='manage-purchase'),
#     path('manage_purchase/<int:pk>',views.manage_purchase,name='manage-purchase-pk'),
#     path('view_purchase',views.view_purchase,name='view-purchase'),
#     path('view_purchase/<int:pk>',views.view_purchase,name='view-purchase-pk'),
#     path('save_purchase',views.save_purchase,name='save-purchase'),
#     path('delete_purchase/<int:pk>',views.delete_purchase,name='delete-purchase'),
#     path('ajax/load-purchase-product/', views.load_purchase_product, name='ajax_load_purchase_product'),
# path('ajax/load-damage-product/', views.load_damage_product, name='ajax_load_damage_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)