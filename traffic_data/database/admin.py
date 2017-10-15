# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Tweet, Hashtag

# Register your models here.

admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Hashtag)