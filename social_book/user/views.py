from django.shortcuts import render, HttpResponse, redirect

# from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import User, file
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
import requests
import json
from django.core import mail
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
import random

# Create your views here.


def home(request):
    # if "token" in request.session:
    #     print(request.session["token"])
    if request.session.get("email") and request.session.get("is_authenticated"):
        return render(request, "index.html")
    else:
        return redirect("loginn")


def otpVerify(request):
    if request.session.get("email") and request.session.get("otp"):
        if request.method == "POST":
            otp = request.POST.get("otp", "")
            if otp == str(request.session["otp"]):
                #  Login Success Mail send
                try:
                    connection = mail.get_connection()
                    connection.open()
                    email1 = mail.EmailMessage(
                        "Hello",
                        "Login Sucessful",
                        "akhterrehan983@gmail.com",
                        [request.session["email"]],
                        connection=connection,
                    )
                    status = email1.send()
                    print(status)
                    connection.close()
                finally:
                    request.session["is_authenticated"] = True
                    return redirect("home")
            else:
                messages.error(request, "Wrong OTP!!!")
                return render(request, "otpVerify.html")
        else:
            return render(request, "otpVerify.html")
    else:
        return redirect("loginn")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/token/login/",
            json={"email": email, "password": password},
        )
        print(response.text)
        if response.status_code == 200:
            response = json.loads(response.text)
            request.session["token"] = response["auth_token"]
            request.session["email"] = email
            number = random.randint(1000, 9999)
            request.session["otp"] = number
            #  otp Mail send
            try:
                connection = mail.get_connection()
                connection.open()
                email1 = mail.EmailMessage(
                    "Hello,This is your One Time Password!!!",
                    str(number),
                    "akhterrehan983@gmail.com",
                    [email],
                    connection=connection,
                )
                status = email1.send()
                print(status)
                connection.close()
                return render(request, "otpVerify.html")
            except:
                del request.session["email"]
                del request.session["otp"]
                del request.session["token"]
                return render(request, "login.html")
        else:
            messages.error(request, "Invalid Credentials!!!")
    return render(request, "login.html")


def logout(request):
    if "email" in request.session:
        del request.session["email"]
    if "auth_token" in request.session:
        del request.session["auth_token"]
    if "otp" in request.session:
        del request.session["otp"]
    if "is_authenticated" in request.session:
        del request.session["is_authenticated"]
    return redirect("loginn")

def register(request):
    if request.method == "POST":
        if request.POST.getlist("checks[]"):
            public_visibility = True
        else:
            public_visibility = False
        print(public_visibility)
        try:
            ob = User(
                email=request.POST.get("email"),
                password=make_password(request.POST.get("pwd")),
                address=request.POST.get("address"),
                public_visibility=public_visibility,
            )
            ob.save()
            messages.success(request, "Registration Successfull!!!")
        except:
            messages.error(request, "Registration Failed!!!")
    return render(request, "register.html")


def authorsAndSellers(request):
    if request.session.get("email") and request.session.get("is_authenticated"):
        users = User.objects.filter(public_visibility=True)
        print(users[0].email)
        return render(request, "index.html", {"users": users})
    else:
        return redirect("loginn")


def upload(request):
    if request.session.get("email") and request.session.get("is_authenticated"):
        if "file" in request.FILES:
            x = request.FILES["file"]

            f = file(email=request.session["email"], upload_to=x)
            f.save()
            return render(request, "index.html")
        else:
            return render(request, "index.html")
    else:
        return redirect("loginn")


def showfiles(request):
    if request.session.get("email") and request.session.get("is_authenticated"):
        response = requests.get(
            "http://127.0.0.1:8000/show",
            headers={"Authorization": "token " + request.session["token"]},
        )
        response = json.loads(response.text)
        files = response.get("files", [])
        print(files)
        return render(request, "index.html", {"files": files})
    else:
        return redirect("loginn")


@api_view(["GET"])
def show(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/users/me/",
        headers={"Authorization": token},
    )
    if response.status_code == 200:
        email = json.loads(response.text)["email"]
        files = file.objects.filter(email=email)
        l = []
        files = list(files)
        for i in range(len(files)):
            l.append(str(files[i].upload_to))
        print(l)
        return Response({"files": l}, status=status.HTTP_200_OK)
    else:
        return Response({"files": []}, status=status.HTTP_401_UNAUTHORIZED)
