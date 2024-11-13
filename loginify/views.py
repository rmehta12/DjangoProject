from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserDetails


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return render(request, "signup.html", {"error": "All fields are required."})

        if UserDetails.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists."})
        if UserDetails.objects.filter(email=email).exists():
            return render(
                request, "signup.html", {"error": "Email already registered."}
            )

        user = UserDetails(username=username, email=email, password=password)
        user.save()
        return redirect("login")

    return render(request, "signup.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "login.html", {"error": "Both fields are required."})

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return render(request, "success.html", {"message": "Login successful!"})
            else:
                return render(request, "login.html", {"error": "Incorrect password."})
        except UserDetails.DoesNotExist:
            return render(request, "login.html", {"error": "User does not exist."})

    return render(request, "login.html")


def get_all_users(request):
    users = UserDetails.objects.all()
    user_data = [
        {"username": user.username, "email": user.email, "password": user.password}
        for user in users
    ]
    return JsonResponse(user_data, safe=False)


def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user_data = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
        return JsonResponse(user_data)
    except UserDetails.DoesNotExist:
        return HttpResponse("User not found", status=404)


def update_user(request, email):
    if request.method == "POST":
        try:
            user = UserDetails.objects.get(email=email)
            user.username = request.POST.get("username", user.username)
            user.password = request.POST.get("password", user.password)
            user.save()
            return HttpResponse("User updated successfully")
        except UserDetails.DoesNotExist:
            return HttpResponse("User not found", status=404)
    return render(request, "update_user.html", {"email": email})


def delete_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        user.delete()
        return HttpResponse("User deleted successfully")
    except UserDetails.DoesNotExist:
        return HttpResponse("User not found", status=404)
