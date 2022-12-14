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
        context['brand'] = {}
    else:
        context['brand'] = models.Brand.objects.get(id=pk)

    return render(request, 'manage_brand.html', context)


def delete_brand(request, pk):
    if request.method == 'GET':
        instance = models.Brand.objects.get(pk=pk)
        models.Brand.objects.filter(pk=instance.pk).delete()
        instance.delete()
        messages.add_message(request, messages.WARNING, 'Brand has been deleted successfully.')
        return redirect('brand-page')


