from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt

from .models import User

def root(request):
    return render(request,'login_app/root_page.html')

def login_page(request):
    if not 'email' in request.session:
        return redirect("/")
    return redirect("/deals")

def logout(request):
    del request.session["first_name"]
    del request.session["email"]
    del request.session["deal"]
    del request.session["sort"]
    return redirect("/")

def login(request):
    all_users=User.objects.all()
    valid_email=False
    for m in all_users:
        if m.email == request.POST["login_email"]:
            valid_email=True
    if valid_email == False:
        messages.error(request,"Doesn't exist",extra_tags="no_email")
        return redirect("/")
    else:
        user= User.objects.get(email=request.POST["login_email"])
        if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
            request.session["first_name"]=user.first_name
            request.session["email"]=request.POST['login_email']
            return redirect("/login_page")
        else:
            messages.error(request,"Wrong Password",extra_tags="wrong_password")
            return redirect("/")

def register(request):
    all_users=User.objects.all()
    valid_email=True
    for m in all_users:
        if m.email == request.POST["email"]:
            valid_email=False
    if valid_email == False:
        messages.error(request,"Already in use",extra_tags="email_inuse")
        return redirect("/")
    errors = User.objects.basic_validation(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value,extra_tags=key)
        return redirect ("/")
    else:
        # PASSWORD HASHING
        form_password = request.POST["password"]
        password_hash=bcrypt.hashpw(form_password.encode(),bcrypt.gensalt())
        request.session["first_name"]=request.POST['first_name']
        request.session["email"]=request.POST['email']
        User.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],email=request.POST["email"],password=password_hash)
        return redirect("/login_page")
