from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

class SubscriptionMiddleware:
    """
    Middleware que bloqueia áreas protegidas para usuários sem assinatura ativa.
    Permite acesso livre a páginas públicas (login, registro, planos, checkout, etc.).
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            reverse("home"),
            reverse('login'),
            reverse('register'),
            # reverse('subscription_plan'),
            # reverse('create_checkout_session'),
            # '/success/',
            # '/cancel/',
        ]

    def __call__(self, request):
        # Permitir acesso a arquivos estáticos
        if request.path.startswith('/static/'):
            return self.get_response(request)
        # Se o caminho for público, deixa passar
        if request.path in self.public_paths:
            return self.get_response(request)
        # Se o usuário não estiver autenticado, o acesso ficará a cargo das views (ex: login_required)
        if not request.user.is_authenticated:
            return redirect('login')
        # Verifica se existe uma assinatura ativa (pode ser trial ou paga)
        active_subscription = request.user.subscriptions.filter(is_active=True, end_date__gt=timezone.now()).first()
        if active_subscription:
            return self.get_response(request)
        # Se não houver assinatura ativa, redireciona para a página de planos
        return redirect('subscription_plan')