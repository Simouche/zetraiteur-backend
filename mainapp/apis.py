from rest_framework.viewsets import ModelViewSet

from mainapp.models import PhoneNumber, Address, Client, Menu, Food, Extra, Composition, OrderLine, Order
from mainapp.serializers import PhoneSerializer, AddressSerializer, ClientSerializer, MenuSerializer, FoodSerializer, \
    ExtraSerializer, CompositionSerializer, OrderLineSerializer, OrderSerializer


class PhoneNumberViewSet(ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneSerializer
    # filterset_class = PhoneNumberFilter


class AddressViewSet(ModelViewSet):
    # filterset_class = AddressFilter
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # filterset_class = ClientFilter


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # filterset_class = MenuFilter


class FoodViewSet(ModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    # filterset_class = FoodFilter


class ExtraViewSet(ModelViewSet):
    serializer_class = ExtraSerializer
    queryset = Extra.objects.all()
    # filterset_class = ExtraFilter


class CompositionViewSet(ModelViewSet):
    serializer_class = CompositionSerializer
    queryset = Composition.objects.all()
    # filterset_class = CompositionFilter


class OrderLineViewSet(ModelViewSet):
    serializer_class = OrderLineSerializer
    queryset = OrderLine.objects.all()
    # filterset_class = OrderLineFilter


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # filterset_class = OrderFilter
