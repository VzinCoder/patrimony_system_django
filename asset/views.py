from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Asset
from department.models import Department
from category.models import Category
from supplier.models import Supplier
from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from .models import Supplier
from .forms import AssetForm
from django.contrib import messages
from movement.models import Movement
from django.core.paginator import Paginator,EmptyPage
# Create your views here.

def delete_asset(request,id):
    asset = get_object_or_404(Asset,pk=id)

    if asset.user != request.user:
        messages.error(request, "Você não tem permissão para deletar este patrimonio.")
        return redirect('assets')
    
    asset.is_deleted = True
    Movement.objects.create(
            user=request.user,
            asset=asset,
            type="exit",
            notes="Patrimonio removido pelo sistema"
    )
    asset.save()
    messages.success(request,f'Patrimonio {asset.name} deletado com sucesso')
    return redirect('assets')

def get_page_assets(request):
    assets = Asset.objects.filter(user=request.user,is_deleted=False).order_by('-id')
    departments = Department.objects.filter(user=request.user)
    suppliers = Supplier.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    template_data = {
        'assets':assets,
        'departments':departments,
        'suppliers':suppliers,
        'categories':categories,
    }

    if request.method != "POST":
       return render(request,"assets.html",template_data)

    id = request.POST.get("id",None)

    if not id:
       form = AssetForm(request.POST,user=request.user)
    else:
       asset_found = get_object_or_404(Asset,pk=id)
       if asset_found.user != request.user:
          messages.error(request, "Você não tem permissão para Atualizar este patrimonio.")
          return redirect('assets')
       form = AssetForm(request.POST,user=request.user,instance=asset_found)

    if form.is_valid():
       asset = form.save()
       action = "Atualizado" if id else "Criado"
       messages.success(request,f'Patrimonio {asset.name} {action} com sucesso')
       return redirect("assets")
    
    template_data["form_update" if id else "form_create"] = form
    return render(request,"assets.html",template_data)
    

def search_suppliers(request):
    search_query = request.GET.get('search', '').strip()
    user = request.user  
    if search_query:
        suppliers = Supplier.objects.filter(
            Q(user=user) & (Q(name__icontains=search_query) | Q(cnpj__icontains=search_query))
        )[:10] 
    else:
        suppliers = Supplier.objects.none()  

    return render(request, 'partials/supplier_results.html', {'suppliers': suppliers})

def get_movements_by_asset(request, asset_id):
    page = request.GET.get('page', 1)
    movements = Movement.objects.filter(user=request.user, asset_id=asset_id).order_by('-id')
    
    paginator = Paginator(movements, 10) 
    try:
        page_obj = paginator.page(page)  
    except EmptyPage:
        return JsonResponse({
            'movements': [],
            'has_next': False
        })
    
    data = {
        'movements': [
            {
                'type': m.get_type_display(),
                'origin': m.origin.name if m.origin else None,
                'destination': m.destination.name if m.destination else None,
                'movement_date': m.movement_date.isoformat(),
            } for m in page_obj
        ],
        'has_next': page_obj.has_next()  # Indica se há mais páginas
    }
    return JsonResponse(data)