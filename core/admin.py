"""
django admin.
"""
from . import models
from django.contrib import admin

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.UserGroup)
