from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from authentication.forms import LoginForm, SignupForm


class IndexView(View):
    template_name = "authentication/index.html"
    message = ""

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect("feed")
            else:
                self.message = (
                    "Incorrect username or password. "
                    "Verify your information and try again."
                )
        return render(
            request,
            self.template_name,
            {"form": form, "message": self.message},
        )


class SignupView(View):
    template_name = "authentication/signup.html"

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return redirect("feed")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
