from .models import Subscription
from django.db import transaction


@transaction.atomic
def create_trial(user):
    trial_subscription = Subscription.objects.create(user=user, plan='trial', is_active=True)
    trial_subscription.set_duration() 
    return trial_subscription
