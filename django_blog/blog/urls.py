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
    path("posts/",                 PostListView.as_view(),   name="posts-list"),
    path("posts/new/",             PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/",        PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/",   PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
