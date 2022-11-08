import json
from collections import ChainMap
from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from configurations import AppConfig

Configs = AppConfig()
client = MongoClient(Configs.getMongoUrl())
db = client.library


def login(request):
    return render(request, "login.html")


def books(request):
    return render(request, "admin.books.html")


def home(request):
    if request.method == "POST":
        req = json.loads(request.body)
        userName = req['userDetails'].get("username")
        password = req['userDetails'].get("password")
        userSearch = [user for user in db.users.find({"username": userName, "isdeleted": {'$nin': ["true", True]}})]
        credentials = dict(ChainMap(*userSearch)) if len(userSearch) > 0 else False
        if credentials is not False and credentials['username'] == userName and credentials['password'] == password:
            return JsonResponse({"message": "hello", "status": "success"})
            # return render(request, "admin.home.html")
        else:
            return JsonResponse({"message": "invalid credentials"})
    else:
        return JsonResponse({"message": "invalid credentials"})


def rent(request):
    return render(request, "admin.rent.html")


def rents(request):
    return render(request, "admin.rents.html")


def userUpdate(request):
    return render(request, "admin.user.update.html")


def users(request):
    return render(request, "admin.users.html")
