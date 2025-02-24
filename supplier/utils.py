from django.shortcuts import render,redirect,get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from django.contrib import messages

def create(request,template_data):
    form = SupplierForm(request.POST,user=request.user)
    if form.is_valid():
       supplier =  form.save()
       messages.success(request, f'Fornecedor {supplier.name} Criado com sucesso')
       return redirect("suppliers")
    
    template_data['form_create'] = form
    return render(request,"suppliers.html",template_data)

def update(request,template_data):
    id_supplier = request.POST.get('id')
    supplier = get_object_or_404(Supplier,pk=id_supplier)

    if supplier.user != request.user:
       messages.error(request, "Você não tem permissão para Atualizar este fornecedor.")
       return redirect('departments')
    
    form = SupplierForm(request.POST, instance=supplier,user=request.user)
    if form.is_valid():
       supplier =  form.save()
       messages.success(request, f'Fornecedor {supplier.name} Atualizado com sucesso')
       return redirect("suppliers")
    
    template_data['form_update'] = form
    return render(request,"suppliers.html",template_data)