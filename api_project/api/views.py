from rest_framework import generics
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Book:
    - list (GET /books_all/)
    - retrieve (GET /books_all/<id>/)
    - create (POST /books_all/)
    - update (PUT /books_all/<id>/)
    - partial_update (PATCH /books_all/<id>/)
    - destroy (DELETE /books_all/<id>/)
    """
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
