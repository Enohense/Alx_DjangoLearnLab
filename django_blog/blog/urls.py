from . import views_auth
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),

    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"),   name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("register/",  profile.register, name="register"),
    path("register/", views_auth.register, name="register"),
]
