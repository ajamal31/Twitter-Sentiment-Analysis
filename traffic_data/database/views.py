# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import databaseController as db
from django.http import HttpResponse


# Create your views here.
def index(request):
    if request.method == 'GET':
        db.updateDatabase()
        return HttpResponse("database updated")