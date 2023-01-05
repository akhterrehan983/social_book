from django.shortcuts import render,HttpResponse
# from django.contrib.auth.models import User
from .models import User
# from .models import userDetails
# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         ob = userDetails(email = request.POST.get('email'),password = request.POST.get('psw'))
#         ob.save()
#         return HttpResponse("user added successfully")

#     else:
#         return render(request,"register.html")  

# def login(request):
#     if request.method == 'POST':
#         if userDetails.objects.filter(email = request.POST.get('email'), password = request.POST.get('psw')):
#             return HttpResponse("login success")
#         else:
#             return HttpResponse("login failed")
#     else:
#         return render(request,"login.html")  



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
        # user = User.objects.create_user()
        # user.email = "new@gmail.com"
        # user.password = "new"
        # user.save()
        return HttpResponse("user added successfully")

    else:
        return render(request,"register.html")  

# def login(request):
#     if request.method == 'POST':
#         pass
#         # if userDetails.objects.filter(email = request.POST.get('email'), password = request.POST.get('psw')):
#         #     return HttpResponse("login success")
#         # else:
#         #     return HttpResponse("login failed")
#     else:
#         # user = User.objects.create_user(email ="new3@gmail.com" ,password = "new3")
#         # user.save()
#         # return HttpResponse("user added successfully")
#         return render(request,"register.html")  

def home(request):
    return render(request,"index.html")

def filterUser(request):
    users = User.objects.filter(public_visibility=True)
    print(users[0].password)
    return render(request,"filterUser.html",{"users":users})