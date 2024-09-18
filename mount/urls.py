from django.urls import path
from .views import *

app_name = "mount"
urlpatterns = [
    path("main", index, name="index"),
    path("download", download, name="download"),
]
