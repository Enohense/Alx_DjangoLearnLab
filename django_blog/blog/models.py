from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )

    class Meta:
        ordering = ["-published_date"]  # newest first

    def __str__(self):
        return f"{self.title} by {self.author}"
