from django.urls import path
from . import views
urlpatterns=[
    path('',views.book_login),
    path('reg',views.register),
    path('home',views.home),
    path('val/<o>/<n>/<e>/<p>',views.home),
    path('add',views.add),
    path('book_logout',views.book_logout),
    path('edit/<pid>',views.edit),

    
] 