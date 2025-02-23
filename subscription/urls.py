from django.contrib import admin
from django.urls import path,include
from .views import create_checkout_session,get_page_subscriptions,stripe_webhook
urlpatterns = [
    path('create-checkout-session',create_checkout_session,name='checkout'),
    path('subscriptions',get_page_subscriptions,name="subscriptions"),
    path("webhook",stripe_webhook,name="webhook")
]