from django.urls import path
from .views import list_books, LibraryDetailView

app_name = "relationship_app"

urlpatterns = [
    path("books/", list_books, name="list-books"),                          # FBV
    path("libraries/<int:pk>/", LibraryDetailView.as_view(),
         name="library-detail"),  # CBV

    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", register, name="register"),
]
