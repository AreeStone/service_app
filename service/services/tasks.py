from celery import shared_task
from django.db.models import F


@shared_task
def set_price(subscrtiption_id):
    from services.models import Subscription

    subscription = Subscription.objects.filter(id=subscrtiption_id).annotate(
        anotated_price=F('service__full_price') -
                       F('service__full_price') * F('plan_discount_percent')/100
    ).first()

    subscription.price = subscription.anotated_price
    subscription.save()