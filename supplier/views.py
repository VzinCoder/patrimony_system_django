from django.shortcuts import render,redirect
from .models import Supplier
from .forms import SupplierForm
from .utils import create,update
from django.contrib import messages
# Create your views here.

def delete_supplier(request):
    pass


def get_page_suppliers(request):
    suppliers = Supplier.objects.filter(user=request.user).order_by('-id')

    template_data = {"suppliers":suppliers}

    if request.method != "POST":
        return render(request,"suppliers.html",template_data)
    
    is_create = not request.POST.get('id')
    params = {'request':request,'template_data':template_data}
    return create(**params) if is_create else update(**params)

