""" Posts urls """
from django.conf.urls import url
# from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    # ?P defines new parameter
    # <fieldname>
    # d+ means accepts only digits
    # with the name parameter we can call this url by that name without building the path
    url(r'^(?P<post_id>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<post_id>\d+)/edit/$', post_update, name='update'),
    url(r'^(?P<post_id>\d+)/delete/$', post_delete, name='delete'),
]
