from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
import json


@ensure_csrf_cookie
def login_page(request):
    return render(request, "login.html")


@login_required
def home_page(request):
    return render(request, "home.html")


def authentication(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = json.loads(request.body)
    email = data["email"]
    password = data["password"]

    if not User.objects.filter(email=email).exists():
        return HttpResponse(
            json.dumps({"error": "A user with this email address does not exist."}),
            status=401,
        )
    else:
        user = authenticate(username=email, password=password)

        if user:
            login(request=request, user=user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(
                content=json.dumps({"error": "You entered the wrong password."}),
                status=401,
            )
