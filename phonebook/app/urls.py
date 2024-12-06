from django.urls import path
from . import views
urlpatterns=[
    path('',views.book_login),
    path('reg',views.register),
    path('home',views.home),
    path('val',views.validate),
    path('add',views.add),
    path('book_logout',views.book_logout),
    path('edit/<pid>',views.edit),
    path('delete/<pid>',views.delete),

    
] 