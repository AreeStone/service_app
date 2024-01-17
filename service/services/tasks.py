import datetime
import time

from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscrtiption_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().filter(id=subscrtiption_id).annotate(
            anotated_price=F('service__full_price') -
                           F('service__full_price') * F('plan__discount_percent') / 100
        ).first()

        subscription.price = subscription.anotated_price
        subscription.save()


@shared_task(base=Singleton)
def set_comment(subscrtiption_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=subscrtiption_id)

        subscription.comment = str(datetime.datetime.now())
        subscription.save()
