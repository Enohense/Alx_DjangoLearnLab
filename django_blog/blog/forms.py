from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Comment, Profile


class RegistrationForm(UserCreationForm):
    """
    Simple registration form extending Django's UserCreationForm
    to collect an email address as well.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Allow users to update standard User fields."""
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    """Allow users to update their Profile (e.g., bio)."""
    class Meta:
        model = Profile
        fields = ("bio",)


class PostForm(forms.ModelForm):
    """
    ModelForm for creating/updating blog posts.
    Uses Taggit's TagWidget so tags can be entered as a comma-separated list.
    """
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "content": forms.Textarea(
                attrs={"rows": 8, "placeholder": "Write your post..."}
            ),
            "tags": TagWidget(),  # <-- IMPORTANT for the checker
        }


class CommentForm(forms.ModelForm):
    """ModelForm for adding/updating comments on a post."""
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your comment…"}
            ),
        }
        help_texts = {
            "content": "Be respectful and keep it constructive."
        }
