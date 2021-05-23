from django.utils.translation import gettext_lazy as _


class ExtraType:
    DESSERT = 'dessert'
    DRINK = 'drink'
    OTHER = 'other'

    CHOICES = (
        (DESSERT, _('Dessert')),
        (DRINK, _('Drink')),
        (OTHER, _('Other'))
    )


class OrderStatus:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PREPARING = 'preparing'
    READY = 'ready'
    ON_DELIVERY = 'on_delivery'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    NO_ANSWER = 'no_answer'
    DITCHED = 'ditched'

    CHOICES = (
        (PENDING, _('Pending')),
        (CONFIRMED, _('Confirmed')),
        (PREPARING, _('Preparing')),
        (READY, _('Ready')),
        (ON_DELIVERY, _('On Delivery')),
        (DELIVERED, _('Delivered')),
        (CANCELED, _('Canceled')),
        (NO_ANSWER, _('No Answer')),
        (DITCHED, _('Ditched')),
    )
