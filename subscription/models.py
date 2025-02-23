from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('trial', 'Teste Gratuito'),
        ('monthly', 'Mensal'),
        ('semiannual', 'Semestral'),
        ('annual', 'Anual'),
    ]
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscriptions'
        )
    
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='trial'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID da assinatura na Stripe"
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID do cliente na Stripe"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Retorna True se a assinatura estiver ativa e não expirada."""
        return self.is_active and self.end_date and self.end_date > timezone.now()
    
    def set_duration(self):
        """Define a data de expiração com base no plano escolhido."""
        now = timezone.now()
        if self.plan == 'trial':
            self.end_date = now + timedelta(days=7)
        elif self.plan == 'monthly':
            self.end_date = now + timedelta(days=30)
        elif self.plan == 'semiannual':
            self.end_date = now + timedelta(days=180)
        elif self.plan == 'annual':
            self.end_date = now + timedelta(days=365)
        self.save()
    
    def cancel(self):
        """Cancela a assinatura."""
        self.is_active = False
        self.save()

    def __str__(self):
        return self.plan