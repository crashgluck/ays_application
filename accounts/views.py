from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.groups.filter(name="Central").exists() or user.is_superuser:
                return redirect("report_views")
            return redirect("inicio")
        messages.error(request, "No pudimos iniciar sesion. Revisa usuario y contrasena.")
    else:
        form = AuthenticationForm()

    form.fields["username"].widget.attrs.update({"class": "form-control", "autofocus": True})
    form.fields["password"].widget.attrs.update({"class": "form-control"})
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "Sesion cerrada correctamente.")
    return redirect("inicio")
