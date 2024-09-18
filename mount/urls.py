from django.urls import path, re_path
from .views import *

app_name = "mount"
urlpatterns = [
    path("", index, name="index"),
    re_path(r'^(?P<path>[^/]+)/$', index, name='index_slug'),
]
