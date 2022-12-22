import json
import datetime
from email import message
from django.shortcuts import render, redirect
from ecommerce import models, forms
from django.contrib import messages
from django.http import HttpResponse


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


def brand(request):
    context = context_data(request)
    context['page'] = 'Brand'
    context['page_title'] = "Brand List"
    context['brands'] = models.Brand.objects.filter(delete_flag=0).all()
    return render(request, 'brand.html', context)


def save_brand(request):
    resp = { 'status': 'failed', 'msg' : '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            brand = models.Brand.objects.get(id = post['id'])
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


def view_brand(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_brand'
    context['page_title'] = 'View Brand'
    if pk is None:
        context['brand'] = {}
    else:
        context['brand'] = models.Brand.objects.get(id=pk)

    return render(request, 'view_brand.html', context)


def manage_brand(request, pk=None):
    context = context_data(request)
    context['page'] = 'manage_brand'
    context['page_title'] = 'Manage Brand'
    if pk is None:
        context['brand'] = {}
    else:
        context['brand'] = models.Brand.objects.get(id=pk)

    return render(request, 'manage_brand.html', context)


def delete_brand(request, pk=None):
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Brand ID is invalid'
    else:
        try:
            models.Brand.objects.filter(pk=pk).update(delete_flag=1)
            messages.success(request, "Brand has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Brand Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def products(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    context['products'] = models.Products.objects.filter(delete_flag = 0).all()
    return render(request, 'products.html', context)


def save_product(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            product = models.Products.objects.get(id = post['id'])
            form = forms.SaveProducts(request.POST, instance=product)
        else:
            form = forms.SaveProducts(request.POST)

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.")
                pid = models.Products.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Product has been updated successfully.")
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


def view_product(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['product'] = {}
        context['stockins'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)
        context['stockins'] = models.StockIn.objects.filter(product__id=pk)
        context['stockouts'] = models.SaleProducts.objects.filter(product__id=pk).order_by('sale__code')

    return render(request, 'view_product.html', context)


def manage_product(request, pk=None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    context['brand'] = models.Brand.objects.filter(delete_flag=0).all()
    if pk is None:
        context['product'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)

    return render(request, 'manage_product.html', context)


def delete_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.Products.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Product has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Product Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def purchase(request):
    context = context_data(request)
    context['page'] = 'purchase'
    context['page_title'] = "Purchase List"
    context['purchases'] = models.Purchase.objects.order_by('-date_added').all()
    return render(request, 'purchase.html', context)


def save_purchase(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            purchase = models.Purchase.objects.get(id = post['id'])
            form = forms.SavePurchase(request.POST, instance=purchase)
        else:
            form = forms.SavePurchase(request.POST)
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Purchase has been saved successfully.")
                pid = models.Purchase.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Purchases has been updated successfully.")
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


def view_purchase(request, pk=None):
    context = context_data(request)
    context['page'] = 'view_purchase'
    context['page_title'] = 'View Purchase'
    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id=pk).all()

    return render(request, 'view_purchase.html', context)


def manage_purchase(request, pk=None):
    context = context_data(request)
    context['page'] = 'manage_purchase'
    context['page_title'] = 'Manage purchase'
    context['brand'] = models.Brand.objects.filter(delete_flag=0).all()
    context['products'] = models.Products.objects.filter(delete_flag=0, status=1).all()

    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id=pk).all()

    return render(request, 'manage_purchase.html', context)


def delete_purchase(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Sale ID is invalid'
    else:
        try:
            models.Purchase.objects.filter(pk = pk).delete()
            messages.success(request, "Purchase has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Purchase Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def load_purchase_product(request):
    brand_id = request.GET.get('brand')
    products = models.Products.objects.filter(brand_id=brand_id, delete_flag=0, status=1).order_by('name')
    context = {'products': products}
    return render(request, 'dropdown_purchase.html', context)


def load_damage_product(request):
    brand_id = request.GET.get('brand')
    products = models.Products.objects.filter(brand_id=brand_id, delete_flag=0, status=1).order_by('name')
    context = {'products': products}
    return render(request, 'dropdown_purchase.html', context)