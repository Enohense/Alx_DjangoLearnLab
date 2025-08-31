from bookshelf.models import Book
count_before = Book.objects.count()
b = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)
b.delete()
count_after = Book.objects.count()
(count_before, count_after)  # (1, 0)
