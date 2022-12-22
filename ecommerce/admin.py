from django.contrib import admin
from ecommerce import models
from django.apps import apps

# Register your models here.
for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
