from django.shortcuts import render

# Create your views here.



def get_categories(request):
    return render(request,'categories.html')