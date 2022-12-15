import json
import datetime
from email import message
from django.shortcuts import render, redirect
from dataset import models, forms
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


def dashboard(request):
    context = context_data(request)
    context['title'] = 'Dashboard'
    context['nav_bar'] = "dashboard"
    return render(request, 'index.html', context)


def brand(request):
    context = context_data(request)
    context['title'] = "Brand"
    context['nav_bar'] = "brand_list"
    context['brands'] = models.Brand.objects.all()
    return render(request, 'brand.html', context)


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


def manage_brand(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Brand'
    context['nav_bar'] = 'manage_brand'
    if pk is None:
        context['brands'] = {}
    else:
        context['brands'] = models.Brand.objects.get(id=pk)

    return render(request, 'manage_brand.html', context)


def delete_brand(request, pk):
    if request.method == 'GET':
        instance = models.Brand.objects.get(pk=pk)
        models.Brand.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Brand has been deleted successfully.')
        return redirect('brand-page')


def package(request):
    context = context_data(request)
    context['title'] = "Package"
    context['nav_bar'] = "package_list"
    context['packages'] = models.Package.objects.all()
    return render(request, 'package.html', context)


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


def manage_package(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Package'
    context['nav_bar'] = 'manage_package'
    if pk is None:
        context['packages'] = {}
    else:
        context['packages'] = models.Package.objects.get(id=pk)

    return render(request, 'manage_package.html', context)


def delete_package(request, pk):
    if request.method == 'GET':
        instance = models.Package.objects.get(pk=pk)
        models.Package.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Package has been deleted successfully.')
        return redirect('package-page')


def unit_set(request):
    context = context_data(request)
    context['title'] = "Unit Set"
    context['nav_bar'] = "unit_sets"
    context['unit_sets'] = models.UnitSet.objects.all()
    return render(request, 'unit_set.html', context)


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


def manage_unit_set(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Unit Set'
    context['nav_bar'] = 'manage_unit_set'
    if pk is None:
        context['unit_sets'] = {}
    else:
        context['unit_sets'] = models.UnitSet.objects.get(id=pk)

    return render(request, 'manage_unit_set.html', context)


def delete_unit_set(request, pk):
    if request.method == 'GET':
        instance = models.UnitSet.objects.get(pk=pk)
        models.UnitSet.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Unit set has been deleted successfully.')
        return redirect('unit-set-page')


def unit_value(request):
    context = context_data(request)
    context['title'] = "Unit Value"
    context['nav_bar'] = "unit_values"
    context['unit_values'] = models.UnitValue.objects.all()
    return render(request, 'unit_value.html', context)


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


def manage_unit_value(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Unit Value'
    context['nav_bar'] = 'manage_unit_value'
    if pk is None:
        context['unit_values'] = {}
    else:
        context['unit_values'] = models.UnitValue.objects.get(id=pk)

    return render(request, 'manage_unit_value.html', context)


def delete_unit_value(request, pk):
    if request.method == 'GET':
        instance = models.UnitValue.objects.get(pk=pk)
        models.UnitValue.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Unit value has been deleted successfully.')
        return redirect('brand-page')


def product(request):
    context = context_data(request)
    context['title'] = "Product"
    context['nav_bar'] = "product_list"
    context['products'] = models.Product.objects.all()
    return render(request, 'product.html', context)


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


def manage_product(request, pk=None):
    context = context_data(request)
    context['title'] = 'Manage Product'
    context['nav_bar'] = 'manage_product'
    if pk is None:
        context['products'] = {}
    else:
        context['products'] = models.Product.objects.get(id=pk)

    return render(request, 'manage_product.html', context)


def delete_product(request, pk):
    if request.method == 'GET':
        instance = models.Product.objects.get(pk=pk)
        models.Product.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.SUCCESS, 'Product has been deleted successfully.')
        return redirect('product-page')


def view_product(request, pk=None):
    context = context_data(request)
    context['title'] = 'Product View'
    context['nav_bar'] = 'product_view'
    if pk is None:
        context['products'] = {}
    else:
        context['products'] = models.Product.objects.get(id=pk)

    return render(request, 'view_product', context)

