from django.shortcuts import render,redirect
from subscription.utils import create_trial
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login,logout as auth_logout
# Create your views here.

def register(request):
    if request.method == "POST":
       form =  UserCreationForm(request.POST)
       if not form.is_valid():
          return render(request,"register.html",{'form':form})
       user = form.save()
       create_trial(user)
       return redirect('login')

    return render(request,"register.html")

def login(request):
   if request.method == "POST":
       form =  AuthenticationForm(data=request.POST)
       if not form.is_valid():
          return render(request,"login.html",{'form':form})
       user = form.get_user()
       auth_login(request,user)
       return redirect('dashboard')

   return render(request,"login.html")


def logout(request):
   auth_logout(request)
   return redirect('login')