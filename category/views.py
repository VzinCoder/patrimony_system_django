from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category
from .forms import CategoryForm

def delete_category(request,id):
    category = get_object_or_404(Category,pk=id)

    if category.user != request.user:
        messages.error(request, "Você não tem permissão para deletar esta categoria.")
        return redirect('categories')
    
    category.delete()
    messages.success(request,f'Categoria {category.name} deletada com sucesso')
    return redirect('categories')

def get_page_categories(request):
    categories = Category.objects.filter(user=request.user).order_by('-id')
    template_data = {'categories': categories}

    if request.method == 'POST':
        id_category = request.POST.get('id', None)

        if id_category:  
            category = get_object_or_404(Category, pk=id_category)

            if category.user != request.user:
                messages.error(request, "Você não tem permissão para Atualizar esta categoria.")
                return redirect('categories')
            
            form = CategoryForm(request.POST, instance=category,user=request.user)
        else: 
            form = CategoryForm(request.POST,user=request.user)

        if form.is_valid():
            category_instance = form.save()
            action = "Atualizada" if id_category else "Criada"
            messages.success(request, f'Categoria {category_instance.name} {action} com sucesso')
            return redirect('categories')

        template_data['form_update' if id_category else 'form_create'] = form

    return render(request, 'categories.html', template_data)