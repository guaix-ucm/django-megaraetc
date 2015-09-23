from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.basic, name='index'),
    url(r'^form$', views.etc_form, name='form'),
    url(r'^do$', views.etc_do, name='results'),
]
