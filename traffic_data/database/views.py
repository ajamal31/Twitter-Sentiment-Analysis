# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import databaseController as db
from django.http import HttpResponse
import json


# Create your views here.
def index(request):
    if request.method == 'GET':
        print 'Get request'
        return HttpResponse(json.dumps({'hi': ' bye'}))
    # db.updateDatabase()
    elif request.method == 'POST':
        print 'Post Request'
        return HttpResponse("post success")
