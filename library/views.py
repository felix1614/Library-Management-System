from django.shortcuts import render


def login(request):
    return render(request, "login.html")


def books(request):
    return render(request, "admin.books.html")


def home(request):
    return render(request, "admin.home.html")


def rent(request):
    return render(request, "admin.rent.html")


def rents(request):
    return render(request, "admin.rents.html")


def userUpdate(request):
    return render(request, "admin.user.update.html")


def users(request):
    return render(request, "admin.users.html")
