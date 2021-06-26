from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import gettext as _

# Create your models here.
from mainapp import ExtraType, OrderStatus


class ZeUser(User):
    username = None
    phone = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_deliveryman = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Client(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(max_length=1000, verbose_name=_('Address'))
    city = models.ForeignKey('City', verbose_name=_('City'), related_name='Clients', on_delete=models.SET_NULL,
                             null=True)
    phone = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(null=True, blank=True)
    verified = models.BooleanField(default=False, verbose_name=_('Verified'))

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def orders_count(self) -> int:
        return self.orders.all().count()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['id']


class PhoneNumber(models.Model):
    phone = models.CharField(max_length=255, unique=True, verbose_name=_('Phone Number'))
    client = models.ForeignKey('Client', verbose_name=_('Client'), on_delete=models.CASCADE, related_name='phones')

    class Meta:
        ordering = ('id',)
        verbose_name = _('Phone Number')
        verbose_name_plural = _('Phone Numbers')

    def __str__(self):
        return self.phone


class City(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    delivery_fee = models.PositiveIntegerField(verbose_name=_('Delivery Fee'), default=0)

    class Meta:
        ordering = ('id',)
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Address(models.Model):
    address = models.TextField(max_length=1000, verbose_name=_('Address'))
    client = models.ForeignKey('Client', verbose_name=_('Client'), on_delete=models.CASCADE, related_name='addresses')
    city = models.ForeignKey('City', verbose_name=_('City'), on_delete=models.SET_NULL, related_name='addresses',
                             null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.address


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    audio_file_name = models.CharField(max_length=255, verbose_name=_('Music'), blank=True)
    available = models.BooleanField(default=True, verbose_name=_('Available'))
    image = models.ImageField(upload_to="images", verbose_name=_('Image'), null=True, blank=True)
    font_name = models.CharField(max_length=255, blank=True, verbose_name=_('Font'))
    price = models.PositiveIntegerField(verbose_name=_('Price'), default=0, blank=True)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    position = models.PositiveIntegerField(default=1, verbose_name=_('Position'))
    menu = models.ForeignKey('Menu', verbose_name=_('Menu'), on_delete=models.CASCADE, related_name="sections")

    class Meta:
        ordering = ('position',)
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return f"{self.menu} > {self.name}"


class Food(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    price = models.PositiveIntegerField(verbose_name=_('Price'), default=0)
    discount_price = models.PositiveIntegerField(verbose_name=_('Discount Price'), null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to="images", verbose_name=_('Image'), blank=True, null=True)
    section = models.ForeignKey('Section', verbose_name=_('Section'), on_delete=models.CASCADE, related_name="foods")

    @property
    def actual_price(self):
        if self.discount_price or self.discount_price != 0:
            return self.discount_price
        if self.price == 0:
            return self.section.menu.price
        return self.price

    class Meta:
        ordering = ('name', 'section__position')
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')

    def __str__(self):
        return self.name


class Extra(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    type = models.CharField(max_length=20, choices=ExtraType.CHOICES, verbose_name=_('Type'), default=ExtraType.OTHER)
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    discount_price = models.PositiveIntegerField(verbose_name=_('Discount Price'), null=True, blank=True)
    image = models.ImageField(upload_to="images", verbose_name=_('Image'), blank=True, null=True)

    @property
    def actual_price(self):
        if self.discount_price or self.discount_price != 0:
            return self.discount_price
        return self.price

    class Meta:
        ordering = ('name', 'type')
        verbose_name = _('Extra')
        verbose_name_plural = _('Extras')

    def __str__(self):
        return self.name


class Composition(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, verbose_name=_('Menu'))
    selected_foods = models.ManyToManyField('Food', through='CompositionFood', through_fields=('composition', 'food',),
                                            verbose_name=_('Selected Foods'), )
    extras = models.ManyToManyField('Extra', verbose_name=_('Extras'), related_name='compositions', )
    cost = models.PositiveIntegerField(verbose_name=_('Cost'), default=0)

    @property
    def actual_cost(self) -> int:
        cost = 0
        for food in self.selected_foods.all():
            cost += food.actual_price
        return cost

    def __str__(self):
        return "{}: {} + {} at {} DZD".format(self.menu,
                                              ", ".join([food.name for food in self.selected_foods.all()]),
                                              ", ".join([extra.name for extra in self.extras.all()]),
                                              self.cost)

    class Meta:
        verbose_name = _('Composition')
        verbose_name_plural = _('Compositions')
        ordering = ('-id',)


class CompositionFood(models.Model):
    food = models.ForeignKey('Food', verbose_name=_('Food'), on_delete=models.CASCADE)
    composition = models.ForeignKey('Composition', verbose_name=_('Composition'), on_delete=models.CASCADE)
    food_price = models.PositiveIntegerField(verbose_name=_('Food Price'), default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.food_price = self.food.actual_price
        super(CompositionFood, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                          update_fields=update_fields)

    class Meta:
        ordering = ('food__section__position',)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    number = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=20, choices=OrderStatus.CHOICES, default=OrderStatus.PENDING)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name="orders", verbose_name=_('Client'))
    phone = models.ForeignKey('PhoneNumber', on_delete=models.CASCADE, related_name="orders", verbose_name=_('Phone'),
                              null=True, blank=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name="orders", verbose_name=_('Address'),
                                null=True, blank=True)

    @property
    def get_phone(self):
        return self.phone or self.client.phone

    @property
    def get_address(self):
        return self.address or self.client.address

    @property
    def items_count(self):
        return self.lines.annotate(count=Sum("quantity")).values("count").get('count', 0)

    @property
    def cost(self):
        cost = 0
        for line in self.lines.all():
            cost += line.total
        return cost

    @staticmethod
    def generate_number():
        from random import randint
        return randint(11111, 99999)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.number = self.generate_number()
        super(Order, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderLine(models.Model):
    composition = models.ForeignKey('Composition', on_delete=models.CASCADE, verbose_name=_('Composition'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'), default=1)
    order = models.ForeignKey('Order', verbose_name=_('Order'), on_delete=models.CASCADE, related_name='lines')

    class Meta:
        ordering = ('id',)

    @property
    def total(self) -> int:
        return self.quantity * self.composition.cost

    def __str__(self):
        return f'({self.composition}) * {self.quantity}'
