# relationship_app/views.py
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library


# --- Function-based view: list all books as plain text ---
def list_books(request):
    """
    Returns a simple text list of all books with their authors.
    """
    books = Book.objects.select_related("author").order_by("title")
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# --- Class-based view: details of a specific library (with books) ---
class LibraryDetailView(DetailView):
    """
    Shows details for a single Library and its books.
    Uses a template: relationship_app/library_detail.html
    """
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # pull books and their authors efficiently
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("books__author")
        )
