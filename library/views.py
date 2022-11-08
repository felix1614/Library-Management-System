import json
import time
from collections import ChainMap
from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from configurations import AppConfig
from datetime import datetime
from django.template.defaulttags import register


Configs = AppConfig()
client = MongoClient(Configs.getMongoUrl())
db = client.library


@register.filter
def get_range(value):
    return range(value)


def login(request):
    return render(request, "login.html")


def books(request):
    Books = [books for books in
                       db.books.find({"isdeleted": {'$nin': ["true", True]}})]
    admin = [admin for admin in
             db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
    admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                              'role': 'unknown'}
    return render(request, "admin.books.html", {"books": Books, "admin": admin})


def home(request):
    if request.method == "POST":
        req = json.loads(request.body)
        userName = req['userDetails'].get("username")
        password = req['userDetails'].get("password")
        userSearch = [user for user in db.users.find({"username": userName, "isdeleted": {'$nin': ["true", True]}, "isadmin":True})]
        credentials = dict(ChainMap(*userSearch)) if len(userSearch) > 0 else False
        if credentials is not False and credentials['username'] == userName and credentials['password'] == password:
            return JsonResponse({"message": "hello", "status": "success"})
            # return render(request, "admin.home.html")
        else:
            return JsonResponse({"message": "invalid credentials"})
    else:
        newArrivalBooks = [books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}, "newArrival":{'$in':[True, "true"]}})]
        userSearch = []
        admin = [admin for admin in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown', 'role': 'unknown'}
        usersQty = 0
        for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin":{'$in':["false", False]}}):
            usersQty += 1
            userDate = datetime.fromtimestamp(int(user["date"]))
            if (datetime.now() - userDate).days <= 15:
                userSearch += user,
        totalBooks = len([books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}})])
        return render(request, 'admin.home.html', {'users': userSearch, 'books': newArrivalBooks, 'total': {'totalUser': usersQty, 'totalBooks':totalBooks}, 'admin': admin})


def rent(request):
    return render(request, "admin.rent.html")


def rents(request):
    return render(request, "admin.rents.html")


def userUpdate(request):
    return render(request, "admin.user.update.html")


def users(request):
    return render(request, "admin.users.html")


def scan(request):
    pass
