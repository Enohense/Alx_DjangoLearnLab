from datetime import date
from rest_framework import serializers
from .models import Author, Book

# BookSerializer: serializes all fields and validates publication_year.


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        """
        Ensure publication_year is not set in the future.
        DRF automatically calls this for the 'publication_year' field.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year {value} cannot be in the future (>{current_year})."
            )
        return value


# AuthorSerializer: includes nested list of the author's books.
# Uses the reverse FK via related_name="books".
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # nested representation

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
