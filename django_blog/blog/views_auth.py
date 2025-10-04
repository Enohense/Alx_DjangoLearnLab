from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "blog/register.html", {"form": form})


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
