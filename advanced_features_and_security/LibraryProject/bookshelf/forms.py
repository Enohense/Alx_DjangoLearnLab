from django import forms
from .models import Book


class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, strip=True)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_year"]

    def clean_published_year(self):
        y = self.cleaned_data.get("published_year")
        if y is not None and (y < 0 or y > 3000):
            raise forms.ValidationError("Year looks invalid.")
        return y
