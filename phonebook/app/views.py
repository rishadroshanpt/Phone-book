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
        # try:
        if UserProfile.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect(register)
        
        otp=OTP(req)
        user_profile = UserProfile.objects.create(name=name,email=email, otp=otp, password=password)

        # user=User.objects.create(first_name=name,email=email,password=password,username=email)
        send_mail('OTP', otp, settings.EMAIL_HOST_USER, [email])
        messages.success(req, "Registration successful. Please check your email for OTP.")
        return redirect(validate)
            # return redirect(book_login)
        # except:
        #     messages.warning(req,'User already exists.')
        #     return redirect(register)
    else:
        return render(req,'register.html')
    
def book_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(book_login)

def validate(req):
    if req.method=='POST':
        uotp=req.POST['uotp']
        try:
            user_profile = UserProfile.objects.get(otp=uotp)
            user = User.objects.create_user(first_name=user_profile.name,email=user_profile.email, username=user_profile.email, password=user_profile.password)  # You can prompt the user to set a password
            user_profile.user = user  # Link the user with the UserProfile
            user_profile.otp_verified = True  # Mark OTP as verified
            user_profile.save()

            # Mark OTP as verified
            # user_profile.otp_verified = True
            # user_profile.save()

            # Log the user in
            # user_profile.user.save()
            # data=user_profile.user
            # data1=User.objects.create(first_name=data.first_name,email=data.email,password=data.password,username=data.email)
            # data1.save()
            # print(data.first_name)

            messages.success(req, "OTP verified successfully. You are now logged in.")
            return redirect(book_login)  # Redirect to the home page after login
        except UserProfile.DoesNotExist:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect(validate)
        # if uotp==otp:
        #     user=User.objects.create_user(first_name=data.uname,email=data.email,password=data.pswd,username=data.email)
        #     user.save()
    else:
        # data=CUser.objects.get(name==id)
        return render(req,'validate.html')

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
            name=req.POST['name'].capitalize()
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
    if req.method=='POST':
        name=req.POST['name'].capitalize()
        phn=req.POST['phn']
        email=req.POST['email']
        place=req.POST['place']
        wa=req.POST['wa']
        Phonebook.objects.filter(pk=pid).update(name=name,phone=phn,email=email,place=place,whatsapp=wa)
        return redirect(home)
    else:
        data=Phonebook.objects.get(pk=pid)
        return render(req,'edit.html',{'data':data})
    
def delete(req,pid):
    data=Phonebook.objects.get(pk=pid)
    data.delete()
    return redirect(home)