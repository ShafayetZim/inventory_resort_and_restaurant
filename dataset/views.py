import json
import datetime
from email import message
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from dataset import models, forms
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView


def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host': abs_uri,
        'page_name': '',
        'nav_bar': '',
        'system_name': 'Eque_Resort',
        'system_short_name': 'EQUE',
        'topbar': True,
        'footer': True,
    }

    return context


@login_required()
def dashboard(request):
    context = context_data(request)
    context['title'] = 'Dashboard'
    context['nav_bar'] = "dashboard"
    context['products'] = models.Product.objects.count()

    context['stock'] = models.Product.objects.all()
    available = 0
    for item in context['stock']:
        available += item.available()
    context['available'] = available

    context['low_stock'] = models.Product.objects.all()
    count = 0
    for item in context['low_stock']:
        if item.available() < 40:
            count = count + 1
    context['count'] = count

    context['sell'] = models.SellSet.objects.filter(date=datetime.date.today())
    sell = 0
    due = 0
    for item in context['sell']:
        sell += item.total_amount
        due += item.due
    context['sell'] = sell
    context['due'] = due

    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    context['month_sell'] = models.SellSet.objects.filter(date_added__month=month,
                                                          date_added__year=year
                                                          ).aggregate(Sum('total_amount'))['total_amount__sum']
    context['month_due'] = models.SellSet.objects.filter(date_added__month=month,
                                                         date_added__year=year
                                                         )
    short = 0
    for item in context['month_due']:
        short += item.short()
    context['short'] = short
    return render(request, 'index.html', context)


@login_required()
def brand(request):
    context = context_data(request)
    context['title'] = "Brand"
    context['nav_bar'] = "brand_list"
    # context['brands'] = models.Brand.objects.all()
    # return render(request, 'dataset/brand.html', context)
    user_preferences = request.user.userpreferences
    if user_preferences.hide_sensitive_content:
        messages.error(request, 'You are not allowed here.')
        return render(request, 'authentication/error.html', context)
    else:
        context['brands'] = models.Brand.objects.all()
        return render(request, 'dataset/brand.html', context)


def save_brand(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            brand = models.Brand.objects.get(id=post['id'])
            form = forms.SaveBrand(request.POST, instance=brand)
        else:
            form = forms.SaveBrand(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Brand has been saved successfully.")
            else:
                messages.success(request, "Brand has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_brand(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Brand'
    context['nav_bar'] = 'manage_brand'
    if request.user.userpreferences.hide_sensitive_content:
        # User has hide_sensitive_content checked, show message or redirect
        messages.error(request, "You are not allowed here.")
        return redirect('dashboard')  # Replace 'home' with the URL to redirect to
    if pk is None:
        context['brand'] = {}
    else:
        context['brand'] = models.Brand.objects.get(id=pk)

    return render(request, 'dataset/manage_brand.html', context)


@login_required()
def delete_brand(request, pk):
    if request.method == 'GET':
        instance = models.Brand.objects.get(pk=pk)
        models.Brand.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Brand has been deleted successfully.')
        return redirect('brand-page')


@login_required()
def package(request):
    context = context_data(request)
    context['title'] = "Package"
    context['nav_bar'] = "package_list"
    context['packages'] = models.Package.objects.all()
    return render(request, 'dataset/package.html', context)


def save_package(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            package = models.Package.objects.get(id=post['id'])
            form = forms.SavePackage(request.POST, instance=package)
        else:
            form = forms.SavePackage(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Package has been saved successfully.")
            else:
                messages.success(request, "Package has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_package(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Package'
    context['nav_bar'] = 'manage_package'
    # Check if the user has the hide_sensitive_content field checked
    if request.user.userpreferences.hide_sensitive_content:
        # Render the error template
        return render(request, 'authentication/error.html', {'message': 'You are not allowed here.'})

    if pk is None:
        context['package'] = {}
    else:
        context['package'] = models.Package.objects.get(id=pk)

    return render(request, 'dataset/manage_package.html', context)


@login_required()
def delete_package(request, pk):
    if request.method == 'GET':
        instance = models.Package.objects.get(pk=pk)
        models.Package.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Package has been deleted successfully.')
        return redirect('package-page')


@login_required()
def unit_set(request):
    context = context_data(request)
    context['title'] = "Unit Set"
    context['nav_bar'] = "unit_sets"
    context['unit_sets'] = models.UnitSet.objects.all()
    return render(request, 'dataset/unit_set.html', context)


def save_unit_set(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            unit_set = models.UnitSet.objects.get(id=post['id'])
            form = forms.SaveUnitSet(request.POST, instance=unit_set)
        else:
            form = forms.SaveUnitSet(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Unit set has been saved successfully.")
            else:
                messages.success(request, "Unit set has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_unit_set(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Unit Set'
    context['nav_bar'] = 'manage_unit_set'
    if pk is None:
        context['unit_set'] = {}
    else:
        context['unit_set'] = models.UnitSet.objects.get(id=pk)

    return render(request, 'dataset/manage_unit_set.html', context)


@login_required()
def delete_unit_set(request, pk):
    if request.method == 'GET':
        instance = models.UnitSet.objects.get(pk=pk)
        models.UnitSet.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Unit set has been deleted successfully.')
        return redirect('unit-set-page')


@login_required()
def unit_value(request):
    context = context_data(request)
    context['title'] = "Unit Value"
    context['nav_bar'] = "unit_values"
    context['unit_values'] = models.UnitValue.objects.all()
    return render(request, 'dataset/unit_value.html', context)


def save_unit_value(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            unit_value = models.UnitValue.objects.get(id=post['id'])
            form = forms.SaveUnitValue(request.POST, instance=unit_value)
        else:
            form = forms.SaveUnitValue(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Unit value has been saved successfully.")
            else:
                messages.success(request, "Unit value has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_unit_value(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Unit Value'
    context['nav_bar'] = 'manage_unit_value'
    context['unit_sets'] = models.UnitSet.objects.all()
    if pk is None:
        context['unit_value'] = {}
    else:
        context['unit_value'] = models.UnitValue.objects.get(id=pk)

    return render(request, 'dataset/manage_unit_value.html', context)


@login_required()
def delete_unit_value(request, pk):
    if request.method == 'GET':
        instance = models.UnitValue.objects.get(pk=pk)
        models.UnitValue.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Unit value has been deleted successfully.')
        return redirect('unit-value-page')


@login_required()
def product(request):
    context = context_data(request)
    context['title'] = "Product"
    context['nav_bar'] = "product_list"
    context['products'] = models.Product.objects.all()
    return render(request, 'product/product.html', context)


@login_required()
def product_price(request):
    context = context_data(request)
    context['title'] = "Product"
    context['nav_bar'] = "dashboard"
    context['products'] = models.Product.objects.all()
    return render(request, 'product/product_recent_price.html', context)


@login_required()
def print_product(request):
    context = context_data(request)
    context['title'] = "Product"
    context['nav_bar'] = "product_list"
    context['products'] = models.Product.objects.all()
    return render(request, 'product/print_product.html', context)


def save_product(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            product = models.Product.objects.get(id=post['id'])
            form = forms.SaveProduct(request.POST, instance=product)
        else:
            form = forms.SaveProduct(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.")
            else:
                messages.success(request, "Product has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_product(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Product'
    context['nav_bar'] = 'manage_product'
    context['brands'] = models.Brand.objects.all()
    context['packages'] = models.Package.objects.all()
    context['unit_sets'] = models.UnitSet.objects.all()
    context['unit_values'] = models.UnitValue.objects.all()
    if pk is None:
        context['product'] = {}
    else:
        context['product'] = models.Product.objects.get(id=pk)

    return render(request, 'product/manage_product.html', context)


@login_required()
def delete_product(request, pk):
    if request.method == 'GET':
        instance = models.Product.objects.get(pk=pk)
        models.Product.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Product has been deleted successfully.')
        return redirect('product-page')


@login_required()
def view_product(request, pk=None):
    context = context_data(request)
    context['title'] = 'Product View'
    context['nav_bar'] = 'product_view'
    if pk is None:
        context['product'] = {}
    else:
        context['product'] = models.Product.objects.get(id=pk)

    return render(request, 'product/view_product.html', context)


@login_required()
def load_unit(request):
    unit_id = request.GET.get('unit')
    values = models.UnitValue.objects.filter(unit_id=unit_id).order_by('value')
    context = {'values': values}
    return render(request, 'product/dropdown_unit.html', context)


@login_required()
def shop(request):
    context = context_data(request)
    context['title'] = "Shop"
    context['nav_bar'] = "shop_list"
    context['shops'] = models.Shop.objects.all()
    return render(request, 'ecommerce/shop.html', context)


def save_shop(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            shop = models.Shop.objects.get(id=post['id'])
            form = forms.SaveShop(request.POST, instance=shop)
        else:
            form = forms.SaveShop(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Shop has been saved successfully.")
            else:
                messages.success(request, "Shop has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_shop(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Shop'
    context['nav_bar'] = 'manage_shop'
    if pk is None:
        context['shop'] = {}
    else:
        context['shop'] = models.Shop.objects.get(id=pk)
    return render(request, 'ecommerce/manage_shop.html', context)


@login_required()
def delete_shop(request, pk):
    if request.method == 'GET':
        instance = models.Shop.objects.get(pk=pk)
        models.Shop.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Shop has been deleted successfully.')
        return redirect('shop-page')


def get_products(request):
    product_id = request.GET.get('product_id')
    products = models.Product.objects.exclude(id=product_id).all()
    data = [{'id': p.id, 'name': p.name} for p in products]
    return JsonResponse(data, safe=False)


@login_required()
def purchase(request):
    context = context_data(request)
    context['title'] = 'Purchase'
    context['nav_bar'] = 'purchase_list'
    context['purchase'] = models.PurchaseSet.objects.order_by('-date_added').all()
    return render(request, 'ecommerce/purchase.html', context)


def save_purchase(request):
    resp = {'status': 'failed', 'msg': '', 'id': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            purchase = models.PurchaseSet.objects.get(id=post['id'])

            form = forms.SavePurchase(request.POST, request.FILES, instance=purchase)
        else:
            form = forms.SavePurchase(request.POST, request.FILES)

            # images = request.FILES.getlist('image')
            # for image in images:
            #     models.PurchaseSet.image.create(image=image)
        if form.is_valid():
            # purchase = form.save()
            # images = request.FILES.getlist('image')
            # for image in images:
            #     purchase.image = image
            #     purchase.save()
            form.save()
            if post['id'] == '':
                messages.success(request, "Purchase has been saved successfully.")
                pid = models.PurchaseSet.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Purchase has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_purchase(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Purchase'
    context['nav_bar'] = 'manage_purchase'
    context['shop'] = models.Shop.objects.all()
    context['products'] = models.Product.objects.all()
    context['payments'] = models.Pay.objects.all()

    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
        context['items'] = {}
    else:
        context['purchase'] = models.PurchaseSet.objects.get(id=pk)
        context['pitems'] = models.PurchaseItem.objects.filter(purchase__id=pk).all()
        context['items'] = models.PurchasePayment.objects.filter(purchase__id=pk).all()

    return render(request, 'ecommerce/manage_purchase.html', context)


@login_required()
def view_purchase(request, pk=None):
    context = context_data(request)
    context['title'] = 'View Purchase'
    context['nav_bar'] = 'view_purchase'

    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
        context['items'] = {}
    else:
        context['purchase'] = models.PurchaseSet.objects.get(id=pk)
        context['pitems'] = models.PurchaseItem.objects.filter(purchase__id=pk).all()
        context['items'] = models.PurchasePayment.objects.filter(purchase__id=pk).all()

    return render(request, 'ecommerce/view_purchase.html', context)


@login_required()
def view_voucher(request, pk=None):
    context = context_data(request)
    context['title'] = 'View Voucher'
    context['nav_bar'] = 'view_voucher'

    if pk is None:
        context['purchase'] = {}
    else:
        context['purchase'] = models.PurchaseSet.objects.get(id=pk)

    return render(request, 'ecommerce/view_voucher.html', context)


@login_required()
def delete_purchase(request, pk):
    if request.method == 'GET':
        instance = models.PurchaseSet.objects.get(pk=pk)
        models.PurchaseSet.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Purchase Set has been deleted successfully.')
        return redirect('purchase-page')


@login_required()
def payment(request):
    context = context_data(request)
    context['title'] = 'Payment'
    context['nav_bar'] = 'payment_list'
    context['payment'] = models.PaymentSet.objects.order_by('-date_added').all()
    return render(request, 'ecommerce/payment.html', context)


def save_payment(request):
    resp = {'status': 'failed', 'msg': '', 'id': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            payment = models.PaymentSet.objects.get(id=post['id'])
            form = forms.SavePayment(request.POST, instance=payment)
        else:
            form = forms.SavePayment(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Payment has been saved successfully.")
                pid = models.PaymentSet.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Payment has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_payment(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Payment'
    context['nav_bar'] = 'manage_payment'
    context['shop'] = models.Shop.objects.all()

    if pk is None:
        context['payment'] = {}
        context['items'] = {}
    else:
        context['payment'] = models.PaymentSet.objects.get(id=pk)
        context['items'] = models.PaymentItem.objects.filter(payment__id=pk).all()

    return render(request, 'ecommerce/manage_payment.html', context)


@login_required()
def view_payment(request, pk=None):
    context = context_data(request)
    context['title'] = 'View Payment'
    context['nav_bar'] = 'view_payment'

    if pk is None:
        context['payment'] = {}
        context['items'] = {}
    else:
        context['payment'] = models.PaymentSet.objects.get(id=pk)
        context['items'] = models.PaymentItem.objects.filter(payment__id=pk).all()

    return render(request, 'ecommerce/view_payment.html', context)


@login_required()
def delete_payment(request, pk):
    if request.method == 'GET':
        instance = models.PaymentSet.objects.get(pk=pk)
        models.PaymentSet.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Payment Set has been deleted successfully.')
        return redirect('payment-page')


@login_required()
def client(request):
    context = context_data(request)
    context['title'] = "Client"
    context['nav_bar'] = "client_list"
    context['clients'] = models.Client.objects.all()
    return render(request, 'ecommerce/client.html', context)


def save_client(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            client = models.Client.objects.get(id=post['id'])
            form = forms.SaveClient(request.POST, instance=shop)
        else:
            form = forms.SaveClient(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Client has been saved successfully.")
            else:
                messages.success(request, "Client has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_client(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Client'
    context['nav_bar'] = 'manage_Client'
    if pk is None:
        context['client'] = {}
    else:
        context['client'] = models.Client.objects.get(id=pk)
    return render(request, 'ecommerce/manage_client.html', context)


@login_required()
def delete_client(request, pk):
    if request.method == 'GET':
        instance = models.Client.objects.get(pk=pk)
        models.Client.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Client has been deleted successfully.')
        return redirect('client-page')


@login_required()
def sell(request):
    context = context_data(request)
    context['title'] = 'Sell'
    context['nav_bar'] = 'sell_list'
    context['sell'] = models.SellSet.objects.order_by('status', '-date_added').all()
    return render(request, 'ecommerce/sell.html', context)


def save_sell(request):
    resp = {'status': 'failed', 'msg': '', 'id': ''}
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            sell = models.SellSet.objects.get(id=post['id'])
            form = forms.SaveSell(request.POST, instance=sell)
        else:
            form = forms.SaveSell(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Sell has been saved successfully.")
                pid = models.SellSet.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Sell has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def manage_sell(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Sell'
    context['nav_bar'] = 'manage_sell'
    context['client'] = models.Client.objects.all()
    context['products'] = models.Product.objects.all()
    if pk is None:
        context['sell'] = {}
        context['pitems'] = {}
    else:
        context['sell'] = models.SellSet.objects.get(id=pk)
        context['pitems'] = models.SellItem.objects.filter(sell_id=pk).all()

    return render(request, 'ecommerce/manage_sell.html', context)


@login_required()
def view_sell(request, pk=None):
    context = context_data(request)
    context['title'] = 'View Sell'
    context['nav_bar'] = 'view_sell'
    if pk is None:
        context['sell'] = {}
        context['pitems'] = {}
    else:
        context['sell'] = models.SellSet.objects.get(id=pk)
        context['pitems'] = models.SellItem.objects.filter(sell__in=pk).all()

    return render(request, 'view_sell.html', context)


@login_required()
def delete_sell(request, pk):
    if request.method == 'GET':
        instance = models.SellSet.objects.get(pk=pk)
        models.SellSet.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, "Sell set has been deleted successfully.")
        return redirect('sell-page')


@login_required()
def view_invoice(request, pk=None):
    context = context_data(request)
    context['title'] = 'View Sell'
    context['nav_bar'] = 'view_sell'
    if pk is None:
        context['sell'] = {}
        context['pitems'] = {}
    else:
        context['sell'] = models.SellSet.objects.get(id=pk)
        context['pitems'] = models.SellItem.objects.filter(sell__id=pk).all()

    return render(request, 'ecommerce/invoice.html', context)


@login_required
def update_transaction_form(request, pk=None):
    context = context_data(request)
    context['page'] = 'update_sell'
    context['title'] = 'Update Status'
    if pk is None:
        context['sell'] = {}
    else:
        context['sell'] = models.SellSet.objects.get(id=pk)

    return render(request, 'ecommerce/update_status.html', context)


def update_transaction_status(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.SellSet.objects.filter(pk=request.POST['id']).update(status=request.POST['status'])
            messages.success(request, "Transaction Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Updating Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required()
def low_stock(request):
    context = context_data(request)
    context['title'] = 'View Low Stock'
    context['nav_bar'] = 'dashboard'
    context['pitems'] = models.Product.objects.all()
    return render(request, 'report/low_stock.html', context)


@login_required()
def client_report(request):
    context = context_data(request)
    context['title'] = 'Client Report'
    context['nav_bar'] = 'client_report'
    context['client'] = models.Client.objects.all()

    request_data = request.GET
    check_client = request_data.get("check_client")
    start_date = request_data.get("start_date")
    end_date = request_data.get("end_date")

    if check_client != "All":
        sell = models.SellSet.objects.filter(client=check_client, date__range=[start_date, end_date])
        items = models.SellItem.objects.filter(sell__in=sell).values(
            'product', 'product__name', 'unit_value', 'price').annotate(
            sum=Sum('total_amount'), qty=Sum('quantity'))
    else:
        sell = models.SellSet.objects.filter(date__range=[start_date, end_date])
        items = models.SellItem.objects.filter(sell__in=sell).values(
            'product', 'product__name', 'unit_value', 'price').annotate(
            sum=Sum('total_amount'), qty=Sum('quantity'))

    context['sell'] = sell
    context['items'] = items
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['check_client'] = check_client
    print(check_client)

    return render(request, 'report/client_report.html', context)


@login_required()
def shop_report(request):
    context = context_data(request)
    context['title'] = 'Shop Report'
    context['nav_bar'] = 'shop_report'
    context['shop'] = models.Shop.objects.all()

    request_data = request.GET
    check_shop = request_data.get("check_shop")
    start_date = request_data.get("start_date")
    end_date = request_data.get("end_date")

    if check_shop != "All":
        purchase_due = models.PurchaseSet.objects.filter(
            shop=check_shop, status=0, date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))
        purchase_paid = models.PurchaseSet.objects.filter(
            shop=check_shop, status=1, date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))
        payment_paid = models.PaymentItem.objects.filter(
            shop=check_shop, date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))

    else:
        purchase_due = models.PurchaseSet.objects.filter(
            date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))
        purchase_paid = models.PurchaseSet.objects.filter(
            date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))
        payment_paid = models.PaymentItem.objects.filter(
            date__range=[start_date, end_date]).values(
            'shop', 'shop__name').annotate(sum=Sum('total_amount'))

    context['purchase_due'] = purchase_due
    context['purchase_paid'] = purchase_paid
    context['payment_paid'] = payment_paid
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['check_shop'] = check_shop
    print(check_shop)

    return render(request, 'report/shop_report.html', context)


@login_required()
def purchase_report(request):
    context = context_data(request)
    context['title'] = 'Purchase Report'
    context['nav_bar'] = 'purchase_report'
    context['shop'] = models.Shop.objects.all()

    request_data = request.GET
    check_shop = request_data.get("check_shop")
    start_date = request_data.get("start_date")
    end_date = request_data.get("end_date")

    if check_shop != "All":
        purchase_due = models.PurchaseSet.objects.filter(
            shop=check_shop, status=0, date__range=[start_date, end_date])
        purchase_paid = models.PurchaseSet.objects.filter(
            shop=check_shop, status=1, date__range=[start_date, end_date])
        payment_paid = models.PaymentItem.objects.filter(
            shop=check_shop, date__range=[start_date, end_date])

    else:
        purchase_due = models.PurchaseSet.objects.filter(
            status=0, date__range=[start_date, end_date])
        purchase_paid = models.PurchaseSet.objects.filter(
            status=1, date__range=[start_date, end_date])
        payment_paid = models.PaymentItem.objects.filter(
            date__range=[start_date, end_date])

    context['purchase_due'] = purchase_due
    context['purchase_paid'] = purchase_paid
    context['payment_paid'] = payment_paid

    due = 0
    paid = 0
    cash = 0
    for item in context['purchase_due']:
        due += float(item.due)
    for item in context['purchase_paid']:
        paid += float(item.due)
    for item in context['payment_paid']:
        cash += float(item.due)

    sub_due = due + paid
    sub_paid = paid + cash
    total_due = due - cash

    context['sub_due'] = sub_due
    context['sub_paid'] = sub_paid
    context['total_due'] = total_due
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['check_shop'] = check_shop
    print(check_shop)

    return render(request, 'report/purchase_report.html', context)


@login_required()
def product_report(request):
    context = context_data(request)
    context['title'] = 'Product Report'
    context['nav_bar'] = 'product_report'
    context['products'] = models.Product.objects.all()

    request_data = request.GET
    check_product = request_data.get("check_product")
    start_date = request_data.get("start_date")
    end_date = request_data.get("end_date")
    product_name = ''
    product_unit = ''

    product_item = models.PurchaseItem.objects.filter(
        product=check_product, date__range=[start_date, end_date])
    if check_product:
        product_name = models.Product.objects.get(id=check_product).name
        product_unit = models.Product.objects.get(id=check_product).unit

    context['product_item'] = product_item
    context['product_name'] = product_name
    context['product_unit'] = product_unit

    qty = 0
    total = 0
    for item in context['product_item']:
        qty += float(item.quantity)
        total += float(item.total_amount)

    context['qty'] = qty
    context['total'] = total
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['check_product'] = check_product

    return render(request, 'report/product_report.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'authentication/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = forms.UserUpdateForm(request.POST, instance=request.user)
        p_form = forms.ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = forms.UserUpdateForm(instance=request.user)
        p_form = forms.ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': "Edit Profile",
        'nav_bar': "profile"
    }
    return render(request, 'authentication/profile.html', context)


@login_required()
def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Account has been created! S/He Can login now.')
            return redirect('all-users')

    else:
        form = forms.UserRegisterForm()

    context = {
        'form': form,
        'title': 'New User',
        'nav_bar': 'new_user',
    }
    return render(request, 'authentication/register.html', context)


@login_required()
def user_list(request):
    context = context_data(request)
    context['title'] = 'User List'
    context['nav_bar'] = 'user_list'
    context['items'] = models.User.objects.filter(is_staff=False).all().order_by('-id')
    return render(request, 'authentication/user_list.html', context)


@login_required()
def user_delete(request, id):
    if request.method == 'GET':
        instance = models.User.objects.get(id=id)
        models.User.objects.filter(id=instance.id).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Delete Success. User has been deleted.')
        return redirect('all-users')


class UserUpdateView(UpdateView):
    model = models.User
    form_class = forms.UpdateUser
    success_url = reverse_lazy('all-users')
    template_name = 'authentication/update_user.html'
    success_message = "User was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User Information"
        context["nav_bar"] = "user_list"
        return context


def user_preferences(request):
    user_preferences, created = models.UserPreferences.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = forms.UserPreferencesForm(request.POST, instance=user_preferences)
        if form.is_valid():
            form.save()
    else:
        form = forms.UserPreferencesForm(instance=user_preferences)
    return render(request, 'authentication/user_preferences.html', {'form': form})

