from django.db import models

# Author: a writer who may have many books.


class Author(models.Model):
    # Human-readable name of the author.
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# Book: a published work written by an Author.
class Book(models.Model):
    # Title of the book.
    title = models.CharField(max_length=255)

    # Year the book was published (simple int for this task).
    publication_year = models.IntegerField()

    # ForeignKey => Many books to one author.
    # related_name="books" lets us access an author's books via author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
