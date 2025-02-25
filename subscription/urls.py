from django.contrib import admin
from django.urls import path,include
from .views import create_checkout_session,get_page_subscriptions,stripe_webhook,get_page_sucess_payment,get_page_error_payment
urlpatterns = [
    path('create-checkout-session',create_checkout_session,name='checkout'),
    path('subscriptions',get_page_subscriptions,name="subscriptions"),
    path('sucess',get_page_sucess_payment,name="payment_sucess"),
    path('error',get_page_error_payment,name="payment_error"),
    path("webhook",stripe_webhook,name="webhook")
]