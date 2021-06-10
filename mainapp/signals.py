from django.db.models.signals import post_save
from django.dispatch import receiver

from mainapp.models import Composition


@receiver(post_save, sender=Composition)
def handle_composition_created(sender, instance, created, **kwargs):
    if instance.cost != instance.actual_cost:
        instance.cost = instance.actual_cost
        instance.save()
