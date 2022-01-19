from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('projects/new', views.new_project, name="new_project"),
]