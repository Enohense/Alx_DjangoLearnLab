from .models import Post, Comment, Tag
from .models import Comment
from .models import Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)


class PostForm(forms.ModelForm):
        tags_csv = forms.CharField(
        required=False,
        label="Tags",
        help_text="Comma-separated (e.g. django, web, tips)"
    )
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "placeholder": "Write your comment…"}),
        }
        help_texts = {"content": "Be respectful and keep it constructive."}



    class Meta:
        model = Post
        # author/published_date handled elsewhere
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill tags_csv when editing
        if self.instance.pk:
            names = self.instance.tags.values_list("name", flat=True)
            self.fields["tags_csv"].initial = ", ".join(names)

    def save(self, commit=True):
        post = super().save(commit=commit)
        # Parse and set tags
        raw = self.cleaned_data.get("tags_csv", "")
        names = [t.strip() for t in raw.split(",") if t.strip()]
        # normalize
        cleaned = []
        for n in names:
            # avoid duplicates with different cases/spaces
            # keep display name as typed; uniqueness is enforced by slug
            cleaned.append(n)

        # build tags and assign
        tags = []
        for name in cleaned:
            slug = slugify(name)
            tag, _ = Tag.objects.get_or_create(
                slug=slug, defaults={"name": name})
            # if tag already exists but name differs in case, keep original name
            tags.append(tag)

        if commit:
            post.tags.set(tags)
        else:
            # if not committed yet, postpone assignment to caller
            self._pending_tags = tags
        return post
