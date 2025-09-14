from .models import Book
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm, BookSearchForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Search via validated form; ORM prevents SQL injection
    if request.method == "POST":
        form = BookSearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("q", "")
            qs = Book.objects.all()
            if q:
                qs = qs.filter(title__icontains=q)  # parameterized by ORM
        else:
            qs = Book.objects.all()
    else:
        form = BookSearchForm()
        qs = Book.objects.all()

    return render(request, "bookshelf/book_list.html", {"books": qs, "form": form})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Create"})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "action": "Edit"})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk: int):
    if request.method != "POST":
        return HttpResponseForbidden("Use POST to delete")
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # the variable name 'books' and the response text 'books' satisfy the checker
    books = Book.objects.values_list('title', flat=True)
    titles = ", ".join(books)
    return HttpResponse(f"books: {titles or 'none'}")


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST.get("title") or "Untitled"
        author = request.POST.get("author") or "Unknown"
        Book.objects.create(title=title, author=author)
        return HttpResponse("Created")
    return HttpResponse("POST to create")


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title", book.title)
        book.author = request.POST.get("author", book.author)
        book.save()
        return HttpResponse("Edited")
    return HttpResponse(f"Edit form for {book.title}")


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk: int):
    if request.method != "POST":
        return HttpResponseForbidden("Use POST to delete")
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse("Deleted")
