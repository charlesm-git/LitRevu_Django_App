from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from authentication.forms import LoginForm, SignupForm


class LoginView(View):
    template_name = "authentication/login.html"

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
                login(request, user)
                return redirect("home")
        return render(request, self.template_name, {"form": form})


class SignupView(View):
    template_name = "authentication/signup.html"

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})
    
class IndexView(View):
    def get(self, request):
        return render(request, 'authentication/index.html')
