
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [path('', views.login, name="login"),
               path(r'^home/$', views.home, name="home"),
               path(r'^rentform/$', views.rent, name="rent"),
               path(r'^books/$', views.books, name="books"),
               path(r'^rental/$', views.rentForm, name="rental"),
               path(r'^returnbook/$', views.returnForm, name="returnbook"),
               path(r'^update/$', views.saveUpdateForm, name="userUpdate"),
               path(r'^users/$', views.users, name="users"),
               path(r'^scan/$', views.scan, name="scan"),
               path(r'^save/$', views.save, name="save")
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
