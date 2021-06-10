from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from mainapp.models import PhoneNumber, Address, Client, Menu, Food, Extra, Composition, OrderLine, Order
from mainapp.serializers import PhoneSerializer, AddressSerializer, ClientSerializer, MenuSerializer, FoodSerializer, \
    ExtraSerializer, CompositionSerializer, OrderLineSerializer, OrderSerializer


class LoginApi(APIView):

    def post(self, request: Request, *args, **kwargs):
        phone = request.data.get('phone', None)
        if phone:
            client: QuerySet[Client] = Client.objects.filter(Q(phone=phone) | Q(phones__phone=phone))
            if client.exists():
                serialized_client = ClientSerializer(client.first(), context=self.get_serializer_context())
                return Response(data=serialized_client.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class PhoneNumberViewSet(ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneSerializer
    lookup_field = 'phone'


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @action(methods=['GET'], detail=False, url_path="client-addresses")
    def get_client_addresses(self, request: Request, *args, **kwargs):
        client = get_object_or_404(Client, phone=request.query_params.get('client', None))
        addresses = self.get_queryset().filter(client=client)
        serialized_data = self.get_serializer(instance=addresses, many=True)
        return Response(serialized_data)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = "phone"


class MenuListView(ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # filterset_class = MenuFilter


class FoodListView(ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    # filterset_class = FoodFilter


class ExtrasListView(ListAPIView):
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
