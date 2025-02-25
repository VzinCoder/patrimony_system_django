import stripe
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Subscription
from django.contrib.auth.models import User
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = request.POST
        price_id = data.get("price_id")

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autorizado'}, status=401)
        
        user = request.user

        active_subscriptions = Subscription.objects.filter(
            user=user,
            is_active=True,
            end_date__gt=timezone.now()
        ).exclude(plan='trial')

        if active_subscriptions.exists():
            return JsonResponse(
                {'error': 'Você já possui uma assinatura ativa.'},
                status=400
            )
        
        try:
            success_url = request.build_absolute_uri(reverse("payment_sucess"))
            cancel_url = request.build_absolute_uri(reverse("payment_error"))
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=user.id,
                metadata={"plan": settings.STRIPE_PRICES_TO_PLAN.get(price_id)}
            )
            return JsonResponse({'sessionId': session.id})
        except Exception as e:
            return JsonResponse({'error': "Error ao tentar criar checkout"}, status=400)
        
@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=404)
    
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_KEY
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  
        client_reference_id = session.get("client_reference_id")
        stripe_customer_id = session.get("customer")
        stripe_subscription_id = session.get('subscription')
        plan = session.get("metadata", {}).get("plan")
        user = User.objects.get(id=client_reference_id)
        subscription = Subscription.objects.create(
            user=user,
            stripe_subscription_id=stripe_subscription_id,
            stripe_customer_id = stripe_customer_id,
            plan = plan
            )
        subscription.set_duration()
    elif event["type"] == "customer.subscription.updated":
       stripe_subscription = stripe.Subscription.retrieve(event['data']['object']['id'])
       try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_subscription.id)
            subscription.set_duration()
       except Subscription.DoesNotExist:
            return HttpResponse(status=404)
    elif event["type"] == "customer.subscription.deleted":
        stripe_subscription = stripe.Subscription.retrieve(event['data']['object']['id'])
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_subscription.id)
            subscription.cancel()
        except Subscription.DoesNotExist:
            return HttpResponse(status=404)
        
    return HttpResponse(status=200)

def get_page_subscriptions(request):
    return render(request,"subscriptions.html",{
        "plans": settings.STRIPE_PRICES,
        "key":settings.STRIPE_PUBLISHABLE_KEY
        })


def  get_page_sucess_payment(request):
    return render(request,"payment_sucess.html")

def  get_page_error_payment(request):
    return render(request,"payment_error.html")