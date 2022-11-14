import base64
import json
import time
from collections import ChainMap
from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from configurations import AppConfig
from datetime import datetime
from django.template.defaulttags import register
from django.conf import settings

from library.models import ImageModel

Configs = AppConfig()
client = MongoClient(Configs.getMongoUrl())
db = client.library


@register.filter
def get_range(value):
    return range(value)


def login(request):
    return render(request, "login.html")


def books(request):
    if request.method == 'POST':
        req = request.POST
        if req['key'] == 'bookArrival':
            Books = []
            for book in db.books.find({"isdeleted": {'$nin': ["true", True]}}):
                bookDate = datetime.fromtimestamp(int(book["date"]))
                if (datetime.now() - bookDate).days <= 15:
                    Books += book,
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            return render(request, "admin.books.html", {"books": Books, "admin": admin, "arrival": "New Arrival"})
    else:
        Books = [books for books in
                           db.books.find({"isdeleted": {'$nin': ["true", True]}})]
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                  'role': 'unknown'}
        return render(request, "admin.books.html", {"books": Books, "admin": admin, "arrival": "All Books"})


def home(request):
    if request.method == "POST":
        req = request.POST
        userName = req["username"]
        password = req["pass"]
        userSearch = [user for user in db.users.find({"username": userName, "isdeleted": {'$nin': ["true", True]}, "isadmin":True})]
        credentials = dict(ChainMap(*userSearch)) if len(userSearch) > 0 else False
        if credentials is not False and credentials['username'] == userName and credentials['password'] == password:
            newArrivalBooks = []
            totalBooks, booksQty = 0, 0
            for book in db.books.find({"isdeleted": {'$nin': ["true", True]}}):
                totalBooks += 1
                bookDate = datetime.fromtimestamp(int(book["date"]))
                if (datetime.now() - bookDate).days <= 15:
                    if booksQty <= 4:
                        newArrivalBooks += book,
                        booksQty += 1
            userSearch = []
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            usersQty, newUser = 0, 0
            for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$in': ["false", False]}}):
                usersQty += 1
                userDate = datetime.fromtimestamp(int(user["date"]))
                if (datetime.now() - userDate).days <= 15:
                    if newUser <= 4:
                        userSearch += user,
                        newUser += 1
            # totalBooks = len([books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}})])
            return render(request, 'admin.home.html', {'users': userSearch, 'books': newArrivalBooks,
                                                       'total': {'totalUser': usersQty, 'totalBooks': totalBooks},
                                                       'admin': admin})
            # return render(request, "admin.home.html")
        else:
            return render(request, 'loginFailed.html')

        # newArrivalBooks = [books for books in db.books.find(
        #     {"isdeleted": {'$nin': ["true", True]}, "newArrival": {'$in': [True, "true"]}})]
        # userSearch = []
        # admin = [admin for admin in
        #          db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        # admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
        #                                                                                           'role': 'unknown'}
        # usersQty = 0
        # for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$in': ["false", False]}}):
        #     usersQty += 1
        #     userDate = datetime.fromtimestamp(int(user["date"]))
        #     if (datetime.now() - userDate).days <= 15:
        #         userSearch += user,
        # totalBooks = len([books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}})])
        # return render(request, 'admin.home.html', {'users': userSearch, 'books': newArrivalBooks,
        #                                            'total': {'totalUser': usersQty, 'totalBooks': totalBooks},
        #                                            'admin': admin})
    else:
        # newArrivalBooks = [books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}, "newArrival":{'$in':[True, "true"]}})]
        # userSearch = []
        # admin = [admin for admin in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        # admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown', 'role': 'unknown'}
        # usersQty = 0
        # for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin":{'$in':["false", False]}}):
        #     usersQty += 1
        #     userDate = datetime.fromtimestamp(int(user["date"]))
        #     if (datetime.now() - userDate).days <= 15:
        #         userSearch += user,
        # totalBooks, booksQty = 0, 0
        # for book in db.books.find({"isdeleted": {'$nin': ["true", True]}}):
        #     totalBooks += 1
        #     bookDate = datetime.fromtimestamp(int(book["date"]))
        #     if (datetime.now() - bookDate).days <= 15:
        #         if booksQty <= 4:
        #             newArrivalBooks += book,
        #             booksQty += 1
        totalBooks, booksQty, newArrivalBooks = 0, 0, []
        for book in db.books.find({"isdeleted": {'$nin': ["true", True]}}):
            totalBooks += 1
            bookDate = datetime.fromtimestamp(int(book["date"]))
            if (datetime.now() - bookDate).days <= 15:
                if booksQty <= 4:
                    newArrivalBooks += book,
                    booksQty += 1
        userSearch = []
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                  'role': 'unknown'}
        usersQty, newUser = 0, 0
        for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$in': ["false", False]}}):
            usersQty += 1
            userDate = datetime.fromtimestamp(int(user["date"]))
            if (datetime.now() - userDate).days <= 15:
                if newUser <= 4:
                    userSearch += user,
                    newUser += 1
        # totalBooks = len([books for books in db.books.find({"isdeleted": {'$nin': ["true", True]}})])
        return render(request, 'admin.home.html', {'users': userSearch, 'books': newArrivalBooks,
                                                   'total': {'totalUser': usersQty, 'totalBooks': totalBooks},
                                                   'admin': admin})
        # return render(request, 'admin.home.html', {'users': userSearch, 'books': newArrivalBooks, 'total': {'totalUser': usersQty, 'totalBooks':totalBooks}, 'admin': admin})


def rent(request):
    return render(request, "admin.rent.html")


def rents(request):
    return render(request, "admin.rentForm.html")


def saveUpdateForm(request):
    if request.method == 'POST':
        req = request.POST
        if req['key'] == 'addUser':
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            options = {"admin": admin, "name": "Add User", "btn": "Add User"}
            return render(request, "admin.user.update.html", options)
        elif req['key'] == 'updateUser':
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            options = {"admin": admin, "name": "Add User", "btn": "Update User"}
            return render(request, "admin.user.update.html", options)

        elif req['key'] == 'addBook':
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            options = {"admin": admin, "name": "Add Book", "btn": "Add Book"}
            return render(request, "admin.book.create.html", options)


def users(request):
    if request.method == 'POST':
        req = request.POST
        if req['key'] == 'newUser':
            users = []
            for user in db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$in': ["false", False]}}):
                userDate = datetime.fromtimestamp(int(user["date"]))
                if (datetime.now() - userDate).days <= 15:
                    users += user,
            admin = [admin for admin in
                     db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
            admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                      'role': 'unknown'}
            return render(request, "admin.users.html", {"users": users, "admin": admin, "arrival": "New Users"})
    else:
        users = [user for user in
                           db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$in': ["false", False]}})]
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                  'role': 'unknown'}
        return render(request, "admin.users.html", {"users": users, "admin": admin, "arrival": "All Users"})


def scan(request):
    pass


def save(request):
    try:
        if request.method == "POST":
            req = request.POST
            if req["key"] == "User":
                userName = req['userName']
                mobile = req["mobile"]
                for user in db.unique_id.find({"key": "user"}):
                    idNum = user['id']+1
                db.unique_id.update({"key": 'user'}, {'$set': {"id": idNum}})
                user_id = f"user_000{idNum}"
                userDate = time.time()
                role = "customer"
                userData = {"username": userName, "isdeleted": False, "isadmin": False, "id": user_id,
                            "date":userDate, "role": role, "mobile": mobile}
                db.users.insert(userData)
                admin = [admin for admin in
                         db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
                admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                          'role': 'unknown'}
                options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "user created successfully", "new": True}
                return render(request, "admin.user.update.html", options)
            else:
                bookName = req['bookName']
                author = req['author']
                cost = int(req['cost'])
                rate = int(req['rate']) if int(req['rate']) >= 1 else 1
                for user in db.unique_id.find({"key": "book"}):
                    idNum = user['id']+1
                db.unique_id.update({"key": 'book'}, {'$set': {"id": idNum}})
                book_id = f"book_000{idNum}"
                bookDate = time.time()
                bookData = {"bookId": book_id, "name": bookName, "author": author, "newArrival": True,
                            "isdeleted": False, "cost": cost, "rate": rate, "date": bookDate}

                db.books.insert(bookData)
                admin = [admin for admin in
                         db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
                admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {
                    'name': 'unknown',
                    'role': 'unknown'}
                options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Book created successfully", "new": True}
                return render(request, "admin.book.create.html", options)

    except Exception as e:
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                  'role': 'unknown'}
        options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Cannot create user", "new": True}
        return render(request, "admin.message.html", options)




