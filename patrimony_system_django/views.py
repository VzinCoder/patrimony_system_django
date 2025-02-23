from django.shortcuts import render,redirect
from django.conf import settings



def get_home(request):
    return render(request,"index.html",{
        "plans": settings.STRIPE_PRICES,
        "key":settings.STRIPE_PUBLISHABLE_KEY
        })