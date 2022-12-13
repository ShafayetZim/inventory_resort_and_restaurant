import json
from django.shortcuts import render, redirect
from dataset import models, forms


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
