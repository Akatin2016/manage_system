from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^insert$', views.insert),
    url(r'^update/(\d+)$', views.update),
    url(r'^upload$', views.upload)
]
