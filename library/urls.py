
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [path('', views.login, name="login"),
               path('home/', views.home, name="home"),
               path('rent/', views.rent, name="rent"),
               path('books/', views.books, name="books"),
               path('rental/', views.rents, name="rental"),
               path('userupdate/', views.userUpdate, name="userUpdate"),
               path('users/', views.users, name="users"),
               path('scan/', views.users, name="scan")
               ]
