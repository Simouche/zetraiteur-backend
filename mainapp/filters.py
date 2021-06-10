import django_filters as filters
from django.db.models import QuerySet, Q

from mainapp.models import Client, Menu, Food, Extra, Order
from django.utils.translation import gettext_lazy as _


class ClientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='full_name', method='filter_full_name', label=_("name"))

    class Meta:
        model = Client
        fields = ('name', 'address', 'phone', 'email', 'verified')

    def filter_full_name(self, queryset: QuerySet['Client'], name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))


class MenuFilter(filters.FilterSet):
    class Meta:
        model = Menu
        fields = ('name', 'audio_file_name', 'available', 'font_name', 'price')


class FoodFilter(filters.FilterSet):
    class Meta:
        model = Food
        fields = ('name', 'price', 'discount_price', 'section', 'section__menu')


class ExtraFilter(filters.FilterSet):
    class Meta:
        model = Extra
        fields = ('name', 'type', 'price', 'discount_price')


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('number', 'created_at', 'status', 'client', 'phone', 'address')
