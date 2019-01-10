from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('admin/',views.admin),
    path('admin/upload/',views.file_upload),
]




