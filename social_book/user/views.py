from django.shortcuts import render,HttpResponse
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate
# from .models import userDetails
# Create your views here.

def home(request):
    if request.session.get('email'):
        return render(request,"index.html")
    else:
        return render(request,"login.html")  

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        user = User.objects.filter(email=email,password=password)
        print(user)
        if user:
            request.session["email"] = email
            return render(request,"index.html")  
        else:
            return HttpResponse("login failed") 
    return render(request,"login.html")  

def logout(request):
    if request.session["email"]:
        del request.session["email"]
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        if request.POST.getlist('checks[]'):
            public_visibility = True
        else:
            public_visibility = False
        print(public_visibility)
        ob = User(email = request.POST.get('email'),password = request.POST.get('pwd'),
        address = request.POST.get('address'),public_visibility=public_visibility)
        ob.save()
        return HttpResponse("user added successfully")

    else:
        return render(request,"register.html")  

def authorsAndSellers(request):
    users = User.objects.filter(public_visibility=True)
    print(users[0].email)
    return render(request,"index.html",{"users":users})

    pass
def filterUser(request):
    users = User.objects.filter(public_visibility=True)
    print(users[0].password)
    return render(request,"filterUser.html",{"users":users})