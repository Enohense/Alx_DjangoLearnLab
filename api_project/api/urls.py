from django.urls import path
from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # List-only view from Task 1
    path('books/', BookList.as_view(), name='book-list'),
    # All CRUD routes for books_all
    path('', include(router.urls)),
]
