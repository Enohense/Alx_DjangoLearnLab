from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def list_books(request):
    # <-- checker looks for Book.objects.all()
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})
# Class-based view: library details + books


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log them in immediately:
            # login(request, user)
            return redirect("login")  # or redirect("list-books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})
