from django.conf.urls import url

import views
from databaseController import updateDatabase

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^updateDatabase$', updateDatabase, name='updateDatabase')
]