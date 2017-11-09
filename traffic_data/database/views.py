# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import database.models
import databaseController as db
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    db.updateDatabase()
    return HttpResponse("Database updated.")

