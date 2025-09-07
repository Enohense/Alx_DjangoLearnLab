from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    # ForeignKey: many Books -> one Author
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
    )

    def __str__(self):
        return f"{self.title} ({self.author.name})"


class Library(models.Model):
    name = models.CharField(max_length=255)
    # ManyToMany: a Library holds many Books; a Book can be in many Libraries
    books = models.ManyToManyField(
        Book,
        related_name="libraries",
        blank=True,
    )

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    # OneToOne: each Library has exactly one Librarian (and vice-versa)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name="librarian",
    )

    def __str__(self):
        return f"{self.name} — {self.library.name}"


# Create your models here.
