from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CommentForm
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import UserUpdateForm, ProfileUpdateForm


def home(request):
    posts = Post.objects.select_related("author").all()
    return render(request, "blog/index.html", {"posts": posts})


@login_required
def profile(request):

    if request.method == "POST":
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()   # save()
            pform.save()   # save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "blog/profile.html", {"uform": uform, "pform": pform})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]  # newest first


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # set author to logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    context_object_name = "post"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# --- Add this inside your existing PostDetailView ---
# (If you already have a PostDetailView, just add get_context_data)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # list of comments for this post
        ctx["comments"] = self.object.comments.select_related("author")
        # empty form for adding a comment (only render in template if authenticated)
        ctx["comment_form"] = CommentForm()
        return ctx


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # Fallback; we’ll submit from post detail
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
