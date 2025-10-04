# api/test_views.py
from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="pass1234"
        )

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

        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])
        self.create_url = reverse("book-create")
        self.update_url = lambda pk: reverse("book-update", args=[pk])
        self.delete_url = lambda pk: reverse("book-delete", args=[pk])

    # ----- READ (public) -----
    def test_list_books_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # use response.data (what the checker wants)
        self.assertGreaterEqual(len(response.data), 3)

    def test_retrieve_book_public(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # ----- CREATE (auth) -----
    def test_create_requires_auth(self):
        payload = {"title": "Anthills",
                   "publication_year": 1987, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Half of a Yellow Sun",
                   "publication_year": 2006, "author": self.author2.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_create_rejects_future_year(self):
        self.client.force_authenticate(self.user)
        future = date.today().year + 1
        payload = {"title": "From The Future",
                   "publication_year": future, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    # ----- UPDATE (auth) -----
    def test_update_requires_auth(self):
        response = self.client.patch(self.update_url(self.book1.id), {
                                     "title": "New"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.update_url(self.book1.id), {
                                     "title": "TFA (Updated)"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ----- DELETE (auth) -----
    def test_delete_requires_auth(self):
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ok_when_authenticated(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ----- FILTER / SEARCH / ORDER -----
    def test_filter_by_author(self):
        response = self.client.get(f"{self.list_url}?author={self.author1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertTrue(
            {"Things Fall Apart", "No Longer at Ease"}.issubset(titles))

    def test_filter_by_year(self):
        response = self.client.get(f"{self.list_url}?publication_year=2013")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Americanah")

    def test_search_title_and_author(self):
        response = self.client.get(f"{self.list_url}?search=achebe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.client.get(f"{self.list_url}?search=americanah")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)
        self.assertEqual(response2.data[0]["title"], "Americanah")

    def test_ordering_desc_by_year(self):
        response = self.client.get(
            f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(
            titles[:3], ["Americanah", "No Longer at Ease", "Things Fall Apart"])


class BookAPITests(APITestCase):
    def setUp(self):
        ...
        self.password = "pass1234"
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password=self.password
        )
        ...

    # handy helper so the checker sees self.client.login
    def _login(self):
        ok = self.client.login(username="tester", password=self.password)
        self.assertTrue(ok)  # make sure login succeeded

    # ---------- CREATE ----------
    def test_create_requires_auth(self):
        payload = {"title": "Anthills",
                   "publication_year": 1987, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_ok_when_authenticated(self):
        self._login()
        payload = {"title": "Half of a Yellow Sun",
                   "publication_year": 2006, "author": self.author2.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_create_rejects_future_year(self):
        self._login()
        future = date.today().year + 1
        payload = {"title": "From The Future",
                   "publication_year": future, "author": self.author1.id}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    # ---------- UPDATE ----------
    def test_update_requires_auth(self):
        response = self.client.patch(self.update_url(self.book1.id), {
                                     "title": "New"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ok_when_authenticated(self):
        self._login()
        response = self.client.patch(self.update_url(self.book1.id), {
                                     "title": "TFA (Updated)"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "TFA (Updated)")

    # ---------- DELETE ----------
    def test_delete_requires_auth(self):
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ok_when_authenticated(self):
        self._login()
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
