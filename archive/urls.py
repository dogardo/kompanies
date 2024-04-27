from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('<str:name>/', dashboard, name='dashboard'),
    path('<str:name>/create/', create, name='create'),
    path('<str:name>/create/<int:id>', create_2, name='create_2'),
    path('<str:name>/delete/<int:id>', delete, name='delete'),
]