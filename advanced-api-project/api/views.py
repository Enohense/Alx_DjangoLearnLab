from .serializers import BookSerializer
from .models import Book
from rest_framework import generics, permissions
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().prefetch_related("books")
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a paginated list of books. Supports simple filtering via query params:
      - ?author=<author_id>
      - ?year=<publication_year>
      - ?q=<substring of title>
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Book.objects.select_related("author").all()
        author_id = self.request.query_params.get("author")
        year = self.request.query_params.get("year")
        q = self.request.query_params.get("q")

        if author_id:
            qs = qs.filter(author_id=author_id)
        if year:
            try:
                qs = qs.filter(publication_year=int(year))
            except ValueError:
                pass
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


# READ-ONLY: anyone can view details
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/
    Retrieve a single book by primary key.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CREATE: authenticated users only
class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Create a new book. Validates payload via BookSerializer, including the
    custom 'publication_year not in future' rule.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Place for server-side business logic/audit hooks if needed.
        serializer.save()


# UPDATE: authenticated users only
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/update/
    Update an existing book. Uses the same serializer validation.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Place for server-side transformations/audit logs.
        serializer.save()


# DELETE: authenticated users only
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/delete/
    Delete a book by primary key.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]
