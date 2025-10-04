"""
Unit tests for the Book API endpoints.

Covers:
- CRUD (list, retrieve, create, update, delete)
- Permissions (read for all, write for authenticated only)
- Validation (publication_year cannot be in the future)
- Filtering (?author=, ?publication_year=, ?title=)
- Searching (?search= on title and author name)
- Ordering (?ordering=title, -publication_year)

Run with:
    python manage.py test api
"""

from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Auth user (for create/update/delete)
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="pass1234"
        )

        # Sample data
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="Chimamanda Ngozi Adichie")

        self.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="No Longer at Ease", publication_year=1960, author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Americanah", publication_year=2013, author=self.author2
        )

        # Named routes from api/urls.py
        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])
        self.create_url = reverse("book-create")
        self.update_url = lambda pk: reverse("book-update", args=[pk])
        self.delete_url = lambda pk: reverse("book-delete", args=[pk])

    # ---------- READ (public) ----------

    def test_list_books_public(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 3)

    def test_retrieve_book_public(self):
        res = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Things Fall Apart")
        self.assertEqual(res.data["publication_year"], 1958)
        self.assertEqual(res.data["author"], self.author1.id)

    # ---------- CREATE (auth) ----------

    def test_create_requires_auth(self):
        payload = {
            "title": "Anthills of the Savannah",
            "publication_year": 1987,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_success_when_authenticated(self):
        self.client.force_authenticate(self.user)
        payload = {
            "title": "Half of a Yellow Sun",
            "publication_year": 2006,
            "author": self.author2.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], payload["title"])
        self.assertEqual(res.data["publication_year"],
                         payload["publication_year"])
        self.assertEqual(res.data["author"], self.author2.id)

    def test_create_rejects_future_year(self):
        self.client.force_authenticate(self.user)
        future = date.today().year + 1
        payload = {"title": "From The Future",
                   "publication_year": future, "author": self.author1.id}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    # ---------- UPDATE (auth) ----------

    def test_update_requires_auth(self):
        res = self.client.patch(self.update_url(self.book1.id), {
                                "title": "New"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_success_when_authenticated(self):
        self.client.force_authenticate(self.user)
        res = self.client.patch(self.update_url(self.book1.id), {
                                "title": "TFA (Updated)"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "TFA (Updated)")

    # ---------- DELETE (auth) ----------

    def test_delete_requires_auth(self):
        res = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_success_when_authenticated(self):
        self.client.force_authenticate(self.user)
        res = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ---------- FILTERING / SEARCH / ORDER ----------

    def test_filter_by_author(self):
        # Only books from author1
        res = self.client.get(f"{self.list_url}?author={self.author1.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in res.data}
        self.assertSetEqual(titles, {"Things Fall Apart", "No Longer at Ease"})

    def test_filter_by_publication_year(self):
        res = self.client.get(f"{self.list_url}?publication_year=2013")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Americanah")

    def test_search_matches_title_or_author(self):
        # Search by author name (case-insensitive, icontains)
        res = self.client.get(f"{self.list_url}?search=achebe")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in res.data}
        self.assertTrue(
            {"Things Fall Apart", "No Longer at Ease"}.issubset(titles))

        # Search by title substring
        res2 = self.client.get(f"{self.list_url}?search=americanah")
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res2.data), 1)
        self.assertEqual(res2.data[0]["title"], "Americanah")

    def test_ordering_by_publication_year_desc(self):
        res = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        returned_titles = [b["title"] for b in res.data]
        expected_order = ["Americanah",
                          "No Longer at Ease", "Things Fall Apart"]
        # Since you may have more than 3 in DB later, check startswith order:
        self.assertEqual(returned_titles[:3], expected_order)
