from django.conf.urls import url

from . import views
from databaseController import updateDatabase

urlpatterns = [
    url(r'^$', views.index, name='index')
]
