from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.get_books, name='get_all_books'),
]