from django.shortcuts import render,redirect
from django.conf import settings
from django.db.models import Count, Q
from django.utils import timezone
from asset.models import Asset
from category.models import Category
from movement.models import Movement
import json
from datetime import timedelta


def get_home(request):
    return render(request,"index.html",{
        "plans": settings.STRIPE_PRICES,
        "key":settings.STRIPE_PUBLISHABLE_KEY
        })


def get_dashboard(request):
    # Filtra todos os dados pelo usuário logado
    user_assets = Asset.objects.filter(user=request.user,is_deleted=False)
    
    # Métricas principais
    total_assets = user_assets.count()
    em_manutencao = user_assets.filter(status=Asset.Status.MAINTENANCE).count()
    
    # Próximos da revisão (considerando assets sem movimentação nos últimos 6 meses)
    seis_meses_atras = timezone.now() - timedelta(days=180)
    proximos_revisao = user_assets.filter(
        Q(movement__movement_date__lte=seis_meses_atras) &
        Q(status=Asset.Status.ACTIVE)
    ).distinct().count()

    # Movimentações do usuário
    user_movements = Movement.objects.filter(user=request.user)
    total_movimentacoes = user_movements.filter(
        movement_date__gte=timezone.now()-timedelta(days=30)
    ).count()
    
    recent_movements = user_movements.select_related('asset', 'origin', 'destination').order_by('-movement_date')[:10]

    # Distribuição por categoria do usuário
    categories = Category.objects.filter(asset__user=request.user, asset__is_deleted=False).annotate(
        total=Count('asset')
    ).distinct()
    
    category_labels = [c.name for c in categories]
    category_data = [c.total for c in categories]

    context = {
        'total_assets': total_assets,
        'em_manutencao': em_manutencao,
        'proximos_revisao': proximos_revisao,
        'total_movimentacoes': total_movimentacoes,
        'recent_movements': recent_movements,
        'category_labels': json.dumps(category_labels),
        'category_data': category_data,
    }
    
    return render(request, "dashboard.html", context)
