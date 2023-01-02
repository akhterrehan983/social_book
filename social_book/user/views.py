from django.shortcuts import render,HttpResponse
from .models import userDetails
# Create your views here.
def register(request):
    if request.method == 'POST':
        ob = userDetails(email = request.POST.get('email'),password = request.POST.get('psw'))
        ob.save()
        return HttpResponse("user added successfully")

    else:
        return render(request,"register.html")  

def login(request):
    if request.method == 'POST':
        if userDetails.objects.filter(email = request.POST.get('email'), password = request.POST.get('psw')):
            return HttpResponse("login success")
        else:
            return HttpResponse("login failed")
    else:
        return render(request,"login.html")  
