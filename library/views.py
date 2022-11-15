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
import requests
Configs = AppConfig()
client = MongoClient(Configs.getMongoUrl())
db = client['library5']

collections = ["unique_id", "users"]
# dblist = client.list_database_names()
for coll in collections:
    if coll in db.list_collection_names():
        pass
    else:
        if coll == "users":
            admin = Configs.adminConfident()
            db.unique_id.insert({"key": "user", "id": 1})
            db.unique_id.insert({"key": "book", "id": 0})
            db.users.insert({"username": admin['user'], "password": str(admin['pass']), "isdeleted": False,
                             "isadmin": True, "id": "user_1", "date": time.time(), "role": "admin", "mobile": str(admin["mobile"])})


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
    if request.method == 'POST':
        req = request.POST
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {
            'name': 'unknown',
            'role': 'unknown'}

        if req['key'] != "rentalForm":
            req = req['key'].split("-")
            if req[0] == 'rentBook':
                for book in db.books.find({"bookId": req[1]}):
                    options = {"admin": admin, "bookDet": book}
                    return render(request, "admin.rent.html", options)
        else:
            req = eval(req['val'])
            book = list(
                map(lambda x: x, db.books.find({"bookId": req["bookId"], "isdeleted": {'$in': ["false", False]}})))
            book = dict(ChainMap(*book)) if len(book) >= 1 else False
            # for book in db.books.find({"bookId": req['bookId'], "isdeleted": {'$in': ["false", False]}}):
            for user in db.users.find({"id": req["userName"], "isdeleted": {'$in': ["false", False]}}):
                options = {"admin": admin, "bookDet": book, "form": True, "det": req}
                return render(request, "admin.rent.html", options)
            else:
                options = {"admin": admin, "msg": "Failed to rent book",
                           "rent": True, "bookDet": book}
                return render(request, "admin.rent.html", options)


def rentForm(request):
    admin = [admin for admin in
             db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
    admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                              'role': 'unknown'}
    options = {"admin": admin, "cat": "Rent Book", "btn": "Add To Shelf"}
    return render(request, "admin.rentForm.html", options)


def returnForm(request):
    admin = [admin for admin in
             db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
    admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                              'role': 'unknown'}
    options = {"admin": admin, "cat": "Return Book", "btn": "Return Book"}
    return render(request, "admin.returnBook.html", options)


def saveUpdateForm(request):
    if request.method == 'POST':
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',                                                                                                  'role': 'unknown'}
        req = request.POST

        if req['key'] == 'addUser':
            options = {"admin": admin, "name": "Add User", "btn": "Add User", "update": False}
            return render(request, "admin.user.update.html", options)

        elif req['key'] == 'updateUser':
            val = req['val']
            for user in db.users.find({"id": val, "isdeleted": {'$in': ["false", False]}}):
                options = {"admin": admin, "name": "Update User", "btn": "Update User", "val": user, "update": True}
                return render(request, "admin.user.update.html", options)

        elif req['key'] == 'addBook':
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


def save(request):
    try:
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {
            'name': 'unknown',
            'role': 'unknown'}
        if request.method == "POST":
            req = request.POST
            if req["key"] == "User":
                try:
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
                    options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "user created successfully", "new": True}
                    return render(request, "admin.user.update.html", options)

                except Exception as en:
                    options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Failed to create User",
                               "new": True}
                    return render(request, "admin.user.update.html", options)
            elif req["key"] == "updateUser":
                try:
                    userName = req['userName']
                    mobile = req["mobile"]
                    userId = req["userId"]
                    userData = {"username": userName, "mobile": mobile}
                    db.users.update({"id": userId}, {'$set': userData})
                    options = {"admin": admin, "name": "Update User", "btn": "Update", "msg": "user Updated successfully", "new": False}
                    return render(request, "admin.user.update.html", options)

                except Exception as en:
                    options = {"admin": admin, "name": "Update User", "btn": "Update", "msg": "Failed to Update User",
                               "new": True}
                    return render(request, "admin.user.update.html", options)
            elif req["key"] == "newBook":
                try:
                    bookName = req['bookName']
                    author = req['author']
                    cost = int(req['cost'])
                    rate = int(req['rate']) if int(req['rate']) >= 1 else 1
                    stock = int(req["stock"])
                    for user in db.unique_id.find({"key": "book"}):
                        idNum = user['id']+1
                    db.unique_id.update({"key": 'book'}, {'$set': {"id": idNum}})
                    book_id = f"book_000{idNum}"
                    bookDate = time.time()
                    bookData = {"bookId": book_id, "name": bookName, "author": author, "newArrival": True,
                                "isdeleted": False, "cost": cost, "rate": rate, "date": bookDate, "stock": stock}

                    db.books.insert(bookData)

                    options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Book created successfully", "new": True}
                    return render(request, "admin.book.create.html", options)
                except Exception as exp:
                    options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Failed to add book",
                               "new": True}
                    return render(request, "admin.book.create.html", options)
            elif req["key"] == "returnBook":
                try:
                    req = req['val']
                    req = eval(req)
                    for rentedBook in db.bookRent.find({"userName": req['userName'], "bookId": req['bookId']}):
                        cost = rentedBook["cost"]
                        date_ = datetime.fromtimestamp(int(rentedBook["date"]))
                        # period = rentedBook["period"]
                        delay = (datetime.now() - date_).days
                        Total = cost * delay if delay >= 1 else cost * 1

                        book = list(map(lambda x: x,
                                        db.books.find({"bookId": rentedBook["bookId"], "isdeleted": {'$in': ["false", False]}})))
                        book = dict(ChainMap(*book)) if len(book) >= 1 else False
                        if book:
                            stock = book["stock"]
                            db.books.update({"bookId": req["bookId"]}, {'$set': {"stock": stock+1}})
                            db.bookRent.update({"userName": req["userName"], "bookId": req["bookId"]},
                                               {'$set': {"returned": True}})

                            options = {"admin": admin, "msg": {"msg": "Book added to library", "Total": Total},
                                       "return": True, "cat": "Return Book", "btn": "Return Book"}
                            return render(request, "admin.returnBook.html", options)
                        else:
                            options = {"admin": admin, "msg": {"msg": "Failed to return book", "Total": ""},
                                       "return": True, "cat": "Return Book", "btn": "Return Book"}
                            return render(request, "admin.returnBook.html", options)

                except Exception as e:
                    options = {"admin": admin, "msg": {"msg": "Failed to return book", "Total": ""},
                               "return": True, "cat": "Return Book", "btn": "Return Book"}
                    return render(request, "admin.returnBook.html", options)

            else:
                try:        # book Rent
                    req = req['val']
                    obj = eval(req)
                    book = list(map(lambda x: x, db.books.find({"bookId": obj["bookId"], "isdeleted": {'$in': ["false", False]}})))
                    book = dict(ChainMap(*book)) if len(book) >= 1 else False
                    for user in db.users.find({"id": obj["userName"], "isdeleted": {'$in': ["false", False]}}):
                        rentaData = {"userName": obj['userName'], "bookId": obj["bookId"], "period": obj["rentDur"],
                                     "duration": int(obj["duration"]) if len(obj['duration']) >= 1 else 1, "returned": False, "date": time.time(), "cost": book["cost"]}
                        db.bookRent.insert(rentaData)
                        # for book in db.books.find({"bookId": obj["bookId"], "isdeleted": {'$in': ["false", False]}}):
                        book["stock"] -= 1
                        db.books.update({"bookId": book['bookId']}, {'$set': {"stock": book['stock']}})
                        options = {"admin": admin, "msg": "book rented successfully",
                                   "rent": True, "bookDet": book}
                        return render(request, "admin.rent.html", options)
                    else:
                        options = {"admin": admin, "msg": "Failed to rent book",
                                   "rent": True, "bookDet": book}
                        return render(request, "admin.rent.html", options)
                except Exception as e:
                    req = req['val']
                    obj = eval(req)
                    for book in db.books.find({"bookId": obj["bookId"]}):
                        options = {"admin": admin, "msg": "book cannot be rented",
                                   "rent": True, "bookDet": book}
                        return render(request, "admin.rent.html", options)

    except Exception as e:
        admin = [admin for admin in
                 db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
        admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                                  'role': 'unknown'}
        options = {"admin": admin, "name": "Add User", "btn": "Create", "msg": "Error 404", "new": True}
        return render(request, "admin.message.html", options)


def scan(request):
    admin = [admin for admin in
             db.users.find({"isdeleted": {'$nin': ["true", True]}, "isadmin": {'$nin': ["false", False]}})]
    admin = {'name': admin[0]['username'], 'role': admin[0]['role']} if len(admin) >= 1 else {'name': 'unknown',
                                                                                              'role': 'unknown'}
    if request.method == "GET":
        return render(request, "admin.scan.html", {"topic": "Scan Books", "admin": admin})
    else:
        try:
            req = request.POST
            req = eval(req['val'])
            books = []

            def requestBook(page):
                url = f"https://frappe.io/api/method/frappe-library?page={page}&title=and"
                response = requests.get(url)
                return response
            page = 1
            cond = True
            while cond:
                if len(books) <= int(req['qty']):
                    response = requestBook(page)

                if response.status_code == 200:
                    responseData = response.json()
                    for book in responseData['message']:
                        if len(books) < int(req['qty']):
                            book['bookId'] = book.pop('bookID')
                            book['name'] = book.pop('title')
                            book['author'] = book.pop('authors')
                            book['newArrival'] = True
                            book['isdeleted'] = False
                            book['cost'] = 20
                            book['rate'] = int(float(book.pop('average_rating')))
                            book['rate'] = int(book['rate'])
                            book['date'] = time.time()
                            book['stock'] = 1
                            books += book,
                        else:
                            cond = False
                            break
                    page += 1

            db.books.insert_many(books)
            options = {"books": books, "admin": admin, "topic": "Scan Books", "scan": True, "msg": "Following books added successfully"}
            return render(request, "admin.scan.html", options)

        except Exception as e:
            options = {"admin": admin, "topic": "Scan Books", "scan": True,
                       "msg": "Failed to Scan Books"}
            return render(request, "admin.scan.html", options)
