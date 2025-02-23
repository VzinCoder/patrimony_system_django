from django.shortcuts import render,redirect,get_object_or_404
from .models import Department
from .forms import DepartmentForm
from django.contrib import messages
# Create your views here.
def delete_department(request,id):
    department = get_object_or_404(Department,pk=id)

    if department.user != request.user:
        messages.error(request, "Você não tem permissão para deletar este departamento.")
        return redirect('departments')
    
    department.delete()
    messages.success(request,f'Departamento {department.name} deletado com sucesso')
    return redirect('departments')

def get_page_departments(request):
    departments = Department.objects.filter(user=request.user).order_by("-id")
    template_data = {"departments":departments}
    if request.method != "POST":
       return render(request,"departments.html",template_data)
    
    id_department = request.POST.get("id")

    # create
    if not id_department:
        form = DepartmentForm(request.POST,user=request.user)
        if form.is_valid():
           department = form.save()
           messages.success(request, f'Departamento {department.name} Criado com sucesso')
           return redirect('departments')
        template_data['form_create'] = form
        return render(request,"departments.html",template_data)

    #update
    department = get_object_or_404(Department, pk=id_department)

    if department.user != request.user:
       messages.error(request, "Você não tem permissão para Atualizar esta categoria.")
       return redirect('departments')

    form =  DepartmentForm(request.POST,user=request.user,instance=department)
    if form.is_valid():
       department = form.save()
       messages.success(request, f'Departamento {department.name} Atualizado com sucesso')
       return redirect('departments')
    template_data['form_update'] = form
    return render(request,"departments.html",template_data)