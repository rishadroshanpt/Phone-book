from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings  
import math,random

# Create your views here.
def book_login(req):
    if 'user' in req.session:
        return redirect(home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(book_login)
    
    else:
        return render(req,'login.html')
    
def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(book_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
        # otp=OTP(req)
        # send_mail('OTP', otp, settings.EMAIL_HOST_USER, [email])
        # return render(req,'validate.html',{'otp':otp,'name':name,'email':email,'password':password})
    else:
        return render(req,'register.html')
    
def book_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(book_login)

# def validate(req,otp,name,email,password):
#     if req.method=='POST':
#         uotp=req.POST['uotp']
#         name=req.POST['name']
#         email=req.POST['email']
#         password=req.POST['password']
#         if uotp==otp:
#             try:
#                 data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
#                 data.save()
#                 return redirect(book_login)
#             except:
#                 messages.warning(req,'User already exists.')
#                 return redirect(register)
#     else:
#         return render(req,'validate.html')

def home(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name=user.first_name
        data = Phonebook.objects.filter(user=user).order_by('name')
        return render(req, 'home.html', {'data': data,'name':name})
    else:
        return redirect('book_login')

def OTP(req) :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
def add(req):
    if 'user' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            phn=req.POST['phn']
            email=req.POST['email']
            place=req.POST['place']
            wa=req.POST['wa']
            user=User.objects.get(username=req.session['user'])
            data=Phonebook.objects.create(user=user,name=name,phone=phn,email=email,place=place,whatsapp=wa)
            data.save()
            return redirect(add)
        else:
            return render(req,'add.html')
    else:
        return redirect(book_login)
    
def edit(req,pid):
    if 'user' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            phn=req.POST['phn']
            email=req.POST['email']
            place=req.POST['place']
            wa=req.POST['wa']
            Phonebook.objects.filter(pk=pid).update(name=name,phone=phn,email=email,place=place,whatsapp=wa)
            return redirect(home)
        else:
            data=Phonebook.objects.get(pk=pid)
            return render(req,'edit.html',{'data':data})
    else:
        return redirect(book_login)