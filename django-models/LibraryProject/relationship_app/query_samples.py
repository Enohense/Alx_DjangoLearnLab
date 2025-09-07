from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name: str):
    """
    Query all books by a specific author.
    """
    qs = Book.objects.filter(author__name=author_name).select_related("author")
    print(f"\nBooks by '{author_name}':")
    if qs.exists():
        for b in qs:
            print(f" - {b.title}")
    else:
        print(" (none found)")
    return qs


def books_in_library(library_name: str):
    """
    List all books in a given library.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"\nLibrary '{library_name}' not found.")
        return Library.objects.none()

    # thanks to related_name="libraries" on Book, we can filter via M2M
    qs = library.books.all().select_related("author")
    print(f"\nBooks in '{library_name}':")
    if qs.exists():
        for b in qs:
            print(f" - {b.title} (by {b.author.name})")
    else:
        print(" (none found)")
    return qs


def librarian_for_library(library_name: str):
    """
    Retrieve the librarian for a library.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"\nLibrary '{library_name}' not found.")
        return None

    # reverse OneToOne via related_name="librarian"
    librarian = getattr(library, "librarian", None)
    print(f"\nLibrarian for '{library_name}':")
    if librarian is None:
        print(" (no librarian assigned)")
    else:
        print(f" - {librarian.name}")
    return librarian


# --- Optional helper to quickly create demo data ---
def seed_demo_data():
    """
    Create a small demo dataset to test queries.
    Safe to run multiple times (uses get_or_create).
    """
    achebe, _ = Author.objects.get_or_create(name="Chinua Achebe")
    adichie, _ = Author.objects.get_or_create(name="Chimamanda Ngozi Adichie")

    tfa, _ = Book.objects.get_or_create(
        title="Things Fall Apart", author=achebe)
    aam, _ = Book.objects.get_or_create(title="Americanah", author=adichie)
    hibs, _ = Book.objects.get_or_create(
        title="Half of a Yellow Sun", author=adichie)

    city_lib, _ = Library.objects.get_or_create(name="City Central Library")
    uni_lib, _ = Library.objects.get_or_create(name="University Library")

    # add books to libraries
    city_lib.books.add(tfa, aam)
    uni_lib.books.add(hibs, tfa)

    Librarian.objects.get_or_create(name="Adaeze Okoye", library=city_lib)
    Librarian.objects.get_or_create(name="Kunle Adeyemi", library=uni_lib)

    print("\nDemo data seeded.")
