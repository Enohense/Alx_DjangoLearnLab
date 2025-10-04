from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
)
from . import views_auth
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),

    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"),   name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("register/", views_auth.register, name="register"),
    path("profile/", views_auth.profile, name="profile"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
