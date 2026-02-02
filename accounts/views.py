from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from core.models import SiteSettings


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("role_redirect")  # Redirect automatico in base al ruolo
        else:
            messages.error(request, "Credenziali non valide.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    settings_obj = SiteSettings.load()

    if not settings_obj.registration_open:
        return render(request, "accounts/registration_closed.html")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registrazione completata. Ora puoi effettuare il login.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def role_redirect(request):
    """Dopo il login, manda l’utente nel dashboard corretto."""
    if request.user.is_staff:
        return redirect("staff_dashboard")
    return redirect("student_dashboard")
