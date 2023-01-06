from django.shortcuts import render,HttpResponse
# from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import User,file
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password,check_password
from rest_framework.decorators import api_view
import requests
import json
# from .models import userDetails
# Create your views here.

def home(request):
    if "token" in request.session:
        print(request.session["token"])
    if request.session.get('email'):
        return render(request,"index.html")
    else:
        return render(request,"login.html")  

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        u = User.objects.filter(email=email)
        # user = User.objects.filter(email=email,password=make_password(password))
        if u:
            password = request.POST.get('pwd')
            if check_password(password,u[0].password):
                request.session["email"] = email
                response = requests.post("http://127.0.0.1:8000/api/v1/token/login",json={"email":email,
    "password":password})
                response = json.loads(response.text)
                request.session["token"] = response["auth_token"]
                return render(request,"index.html")  
            else:
                return HttpResponse("login failed") 
        else:
            return HttpResponse("login failed") 
    return render(request,"login.html")  

def logout(request):
    if "email" in request.session:
        del request.session["email"]
    if "auth_token" in request.session:
        del request.session["auth_token"]
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        if request.POST.getlist('checks[]'):
            public_visibility = True
        else:
            public_visibility = False
        print(public_visibility)
        ob = User(email = request.POST.get('email'),password = make_password(request.POST.get('pwd')),
        address = request.POST.get('address'),public_visibility=public_visibility)
        ob.save()
        return HttpResponse("user added successfully")

    else:
        return render(request,"register.html")  

def authorsAndSellers(request):
    users = User.objects.filter(public_visibility=True)
    print(users[0].email)
    return render(request,"index.html",{"users":users})

def filterUser(request):
    users = User.objects.filter(public_visibility=True)
    print(users[0].password)
    return render(request,"filterUser.html",{"users":users})

def upload(request):
    x = request.FILES["file"]

    f = file(email = request.session["email"], upload_to=x)
    f.save()

    return render(request, "index.html")


def show(request):
    files = file.objects.filter(email=request.session["email"])
    l = []
    response = requests.get("http://127.0.0.1:8000/authenticate",headers={"Authorization":"token "+request.session["token"]})
    # print(response)
    response = json.loads(response.text)
    if response['detail'] == "Valid token":
        files = list(files)
        for i in range(len(files)):
            l.append(str(files[i].upload_to))
        return render(request, "index.html", {"files": l})
    return render(request, "index.html")

@api_view(["GET"])
def authenticate(request):
    return JsonResponse({"detail":'Valid token'})