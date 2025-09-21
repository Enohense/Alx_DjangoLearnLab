from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly


class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    # inherits global IsAuthenticatedOrReadOnly (read for all)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]   # ← overrides global default
    # authentication uses settings.py defaults (Token/Session)
