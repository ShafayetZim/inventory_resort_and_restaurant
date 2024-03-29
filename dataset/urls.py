from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('get_products/', views.get_products, name='get_products'),
    # crud urls for authentication
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('register', views.register, name='register'),
    path('all_user', views.user_list, name="all-users"),
    path('user_delete/<int:id>', views.user_delete, name="user-delete"),
    path('update_user/<int:pk>', views.UserUpdateView.as_view(), name='update_user'),
    path('preferences', views.user_preferences, name='user_preferences'),
    # crud urls for brand
    path('brand', views.brand, name='brand-page'),
    path('manage_brand', views.manage_brand, name='manage-brand'),
    path('manage_brand/<int:pk>', views.manage_brand, name='manage-brand-pk'),
    path('save_brand', views.save_brand, name='save-brand'),
    path('delete_brand/<int:pk>', views.delete_brand, name='delete-brand'),
    # crud urls for package
    path('package', views.package, name='package-page'),
    path('manage_package', views.manage_package, name='manage-package'),
    path('manage_package/<int:pk>', views.manage_package, name='manage-package-pk'),
    path('save_package', views.save_package, name='save-package'),
    path('delete_package/<int:pk>', views.delete_package, name='delete-package'),
    # crud urls for unit set
    path('unit_set', views.unit_set, name='unit-set-page'),
    path('manage_set', views.manage_unit_set, name='manage-unit-set'),
    path('manage_unit_set/<int:pk>', views.manage_unit_set, name='manage-unit-set-pk'),
    path('save_unit_set', views.save_unit_set, name='save-unit-set'),
    path('delete_unit_set/<int:pk>', views.delete_unit_set, name='delete-unit-set'),
    # crud urls for unit value
    path('unit_value', views.unit_value, name='unit-value-page'),
    path('manage_unit_value', views.manage_unit_value, name='manage-unit-value'),
    path('manage_unit_value/<int:pk>', views.manage_unit_value, name='manage-unit-value-pk'),
    path('save_unit_value', views.save_unit_value, name='save-unit-value'),
    path('delete_unit_value/<int:pk>', views.delete_unit_value, name='delete-unit-value'),
    # crud urls for product
    path('product', views.product, name='product-page'),
    path('product_price', views.product_price, name='product-price'),
    path('product_print', views.print_product, name='product-print'),
    path('manage_product', views.manage_product, name='manage-product'),
    path('manage_product/<int:pk>', views.manage_product, name='manage-product-pk'),
    path('save_product', views.save_product, name='save-product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete-product'),
    path('view_product', views.view_product, name='view-product'),
    path('view_product/<int:pk>', views.view_product, name='view-product-pk'),
    path('ajax/load-unit/', views.load_unit, name='ajax_load_unit'),
    # crud urls for shop
    path('shop', views.shop, name='shop-page'),
    path('manage_shop', views.manage_shop, name='manage-shop'),
    path('manage_shop/<int:pk>', views.manage_shop, name='manage-shop-pk'),
    path('save_shop', views.save_shop, name='save-shop'),
    path('delete_shop/<int:pk>', views.delete_shop, name='delete-shop'),
    # crud urls for purchase
    path('purchase', views.purchase, name='purchase-page'),
    path('manage_purchase', views.manage_purchase, name='manage-purchase'),
    path('manage_purchase/<int:pk>', views.manage_purchase, name='manage-purchase-pk'),
    path('save_purchase', views.save_purchase, name='save-purchase'),
    path('delete_purchase/<int:pk>', views.delete_purchase, name='delete-purchase'),
    path('view_purchase', views.view_purchase, name='view-purchase'),
    path('view_purchase/<int:pk>', views.view_purchase, name='view-purchase-pk'),
    path('view_voucher', views.view_voucher, name='view-voucher'),
    path('view_voucher/<int:pk>', views.view_voucher, name='view-voucher-pk'),
    # crud urls for payment
    path('payment', views.payment, name='payment-page'),
    path('manage_payment', views.manage_payment, name='manage-payment'),
    path('manage_payment/<int:pk>', views.manage_payment, name='manage-payment-pk'),
    path('save_payment', views.save_payment, name='save-payment'),
    path('delete_payment/<int:pk>', views.delete_payment, name='delete-payment'),
    path('view_payment', views.view_payment, name='view-payment'),
    path('view_payment/<int:pk>', views.view_payment, name='view-payment-pk'),
    # crud urls for client
    path('client', views.client, name='client-page'),
    path('manage_client', views.manage_client, name='manage-client'),
    path('manage_client/<int:pk>', views.manage_client, name='manage-client-pk'),
    path('save_client', views.save_client, name='save-client'),
    path('delete_client/<int:pk>', views.delete_client, name='delete-client'),
    # crud urls for sell
    path('sell', views.sell, name='sell-page'),
    path('manage_sell', views.manage_sell, name='manage-sell'),
    path('manage_sell/<int:pk>', views.manage_sell, name='manage-sell-pk'),
    path('save_sell', views.save_sell, name='save-sell'),
    path('delete_sell/<int:pk>', views.delete_sell, name='delete-sell'),
    path('view_sell', views.view_sell, name='view-sell'),
    path('view_sell/<int:pk>', views.view_sell, name='view-sell-pk'),
    path('view_invoice', views.view_invoice, name='view-invoice'),
    path('view_invoice/<int:pk>', views.view_invoice, name='view-invoice-pk'),
    path('update_transaction_form/<int:pk>', views.update_transaction_form, name='transaction-update-status'),
    path('update_transaction_status', views.update_transaction_status, name='update-sale-status'),
    # report
    path('low_stock', views.low_stock, name='low-stock'),
    path('client_report', views.client_report, name='client-report'),
    path('shop_report', views.shop_report, name='shop-report'),
    path('purchase_report', views.purchase_report, name='purchase-report'),
    path('product_report', views.product_report, name='product-report'),
    path('stock_report', views.stock_report, name='stock-report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
