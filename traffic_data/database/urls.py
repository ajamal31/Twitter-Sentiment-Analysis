from django.conf.urls import url

import views
from databaseController import updateDatabase

urlpatterns = [
    url(r'^$', views.index, name='index')
]
