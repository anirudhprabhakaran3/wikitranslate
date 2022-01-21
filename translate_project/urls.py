from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('', auth_views.LoginView.as_view(next_page='dashboard', redirect_authenticated_user=True), name="login"),
    path('login', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path('signup', views.signup, name="signup"),

    # Project Admin URLs
    path('projects/admin', views.admin_page, name="admin_page"),
    path('projects/admin/projects', views.admin_projects, name="admin_projects"),
    path('projects/admin/projects/<int:project_pk>/assign_translator', views.assign_translator, name="assign_translator"),
    path('projects/admin/translators', views.admin_translators, name="admin_translators"),
    path('projects/admin/translators/<int:translator_pk>/change_permissions', views.change_permissions, name="change_permissions"),

    # Project URLs
    path('dashboard', views.dashboard, name="dashboard"),
    path('projects/<int:project_pk>', views.view_project, name="view_project"),
    path('projects/new', views.new_project, name="new_project"),
    path('projects/<int:project_pk>/translate', views.translate, name="translate"),

    # API URLs
    path('api/submit_translation', views.submit_translation, name="submit_translation"),
]