from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

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
            reverse('subscriptions'),
            reverse('checkout'),
            reverse("webhook")
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
        # Permitir acesso ao login da área de administração
        if request.path.startswith('/admin/login'):
            return self.get_response(request)
        # Redirecionar o usuario para tela de login caso ele nao esteja logado
        if not request.user.is_authenticated:
            return redirect('login')
        # Permitir acesso à área de administração para usuários com permissão de admin
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)
        # Verifica se existe uma assinatura ativa (pode ser trial ou paga)
        active_subscription = request.user.subscriptions.filter(is_active=True, end_date__gt=timezone.now()).first()
        if active_subscription:
            return self.get_response(request)
        # Se a assinatura não estiver ativa, envia uma mensagem flash
        messages.error(request, "Seu plano de assinatura expirou. Por favor, renove para continuar acessando o sistema.")
        return redirect('subscriptions')