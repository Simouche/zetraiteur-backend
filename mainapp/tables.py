import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from mainapp.models import Client, Menu, Food, Extra, Order

ROW_ATTRS = {
    "data-id": lambda record: record.pk,
}
ATTRS = {
    "class": "table table-borderless table-striped table-earning"
}
EMPTY_TEXT = _('Empty')


class TableWithActionsMixin(tables.Table):
    actions = tables.TemplateColumn(template_name="dashboard/table_templates/actions_buttons.html",
                                    verbose_name=_('Actions'), )


class ClientTable(TableWithActionsMixin, tables.Table):
    full_name = tables.Column(order_by=('first_name', 'last_name'), verbose_name=_('Name'))

    class Meta:
        model = Client
        fields = ('full_name', 'phone', 'email', 'verified')
        empty_text = EMPTY_TEXT
        row_attrs = ROW_ATTRS
        attrs = ATTRS


class MenuTable(TableWithActionsMixin, tables.Table):
    image = tables.TemplateColumn('<img width="64px" src="{{record.image.url}}"> ')

    class Meta:
        model = Menu
        fields = ('image', 'name', 'audio_file_name', 'font_name', 'available', 'price')
        empty_text = EMPTY_TEXT
        row_attrs = ROW_ATTRS
        attrs = ATTRS


class FoodTable(TableWithActionsMixin, tables.Table):
    image = tables.TemplateColumn('<img width="64px" src="{{record.image.url}}"> ')
    actual_price = tables.Column(order_by=('price', 'discount_price'), verbose_name=_('Actual Price'))

    class Meta:
        model = Food
        fields = ('image', 'name', 'price', 'discount_price', 'actual_price', 'section__name')
        empty_text = EMPTY_TEXT
        row_attrs = ROW_ATTRS
        attrs = ATTRS


class ExtraTable(TableWithActionsMixin, tables.Table):
    image = tables.TemplateColumn('<img width="64px" src="{{record.image.url}}"> ')
    actual_price = tables.Column(order_by=('price', 'discount_price'), verbose_name=_('Actual Price'))

    class Meta:
        model = Extra
        fields = ('image', 'name', 'type', 'price', 'discount_price', 'actual_price',)
        empty_text = EMPTY_TEXT
        row_attrs = ROW_ATTRS
        attrs = ATTRS


class OrderTable(TableWithActionsMixin, tables.Table):
    client = tables.Column(verbose_name=_('Client'), )
    get_phone = tables.Column(verbose_name=_('Phone'))
    get_address = tables.Column(verbose_name=_('Address'))
    items_count = tables.Column(verbose_name=_('Items'))

    class Meta:
        model = Order
        fields = ('number', 'client', 'get_phone', 'get_address', 'cost', 'items_count')
        empty_text = EMPTY_TEXT
        row_attrs = ROW_ATTRS
        attrs = ATTRS
