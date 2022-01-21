from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('projects/<int:project_pk>', views.view_project, name="view_project"),
    path('projects/new', views.new_project, name="new_project"),
    path('projects/<int:project_pk>/translate', views.translate, name="translate"),
    path('api/submit_translation', views.submit_translation, name="submit_translation"),
]