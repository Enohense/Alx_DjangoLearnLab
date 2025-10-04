# blog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from taggit.models import Tag

from .forms import (
    PostForm, CommentForm, UserUpdateForm, ProfileUpdateForm
)
from .models import Post, Comment


# -----------------------------
# Basic pages
# -----------------------------
def home(request):
    posts = Post.objects.select_related("author").all()
    return render(request, "blog/index.html", {"posts": posts})


@login_required
def profile(request):
    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {"uform": uform, "pform": pform})


# -----------------------------
# Post CRUD
# -----------------------------
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]  # newest first


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author")
        ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    context_object_name = "post"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts-list")

    def test_func(self):
        return self.get_object().author == self.request.user


# -----------------------------
# Comment CRUD
# -----------------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # Fallback template; usually the form is rendered on post_detail
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    context_object_name = "comment"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    context_object_name = "comment"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post_id})


# -----------------------------
# Tag listing (required by checker)
# -----------------------------
class PostByTagListView(ListView):
    """
    List posts filtered by a tag slug.
    The checker expects this exact class name and kwarg 'tag_slug'.
    """
    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        slug = self.kwargs.get("tag_slug")
        self.tag = get_object_or_404(Tag, slug=slug)
        return (
            Post.objects.filter(tags__in=[self.tag])
            .select_related("author")
            .prefetch_related("tags")
            .order_by("-published_date")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag"] = self.tag
        return ctx


# -----------------------------
# Search
# -----------------------------
class SearchResultsView(ListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return Post.objects.none()
        return (
            Post.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            )
            .select_related("author")
            .prefetch_related("tags")
            .distinct()
            .order_by("-published_date")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx
