from django.urls import path
from .views import list_books, LibraryDetailView

app_name = "relationship_app"

urlpatterns = [
    # function-based view
    path("books/", list_books, name="list-books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(),
         name="library-detail"),  # class-based view
]
