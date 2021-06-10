from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from mainapp.models import Client, PhoneNumber, Address, Menu, Section, Food, Extra, Composition, OrderLine, Order, \
    City, CompositionFood


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'delivery_fee')
        extra_kwargs = {
            'id': {'read_only': True, },
        }


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'client', 'phone')
        extra_kwargs = {
            'id': {'read_only': True, },
            'client': {'required': False, },
        }


class AddressSerializer(ModelSerializer):
    city_obj = CitySerializer(read_only=True, source='city')

    class Meta:
        model = Address
        fields = ('id', 'client', 'address', 'city', 'city_obj')
        extra_kwargs = {
            'id': {'read_only': True, },
            'client': {'required': False, },
            'city': {'write_only': True, },
        }


class ClientSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    city_obj = CitySerializer(read_only=True, source='city')

    def create(self, validated_data):
        phones = validated_data.pop('phones') if validated_data.get('phones') else []
        addresses = validated_data.pop('addresses') if validated_data.get('addresses') else []
        client = super(ClientSerializer, self).create(validated_data)

        for phone in phones:
            PhoneNumber.objects.create(client=client, **phone)

        for address in addresses:
            Address.objects.create(client=client, **address)
        return client

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'address', 'phone', 'email', 'phones', 'addresses', 'city',
                  'city_obj')
        extra_kwargs = {
            'id': {'read_only': True, },
            'city': {'write_only': True, },
        }


class FoodSerializer(ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'discount_price', 'description', 'image', 'section')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class SectionSerializer(ModelSerializer):
    foods = FoodSerializer(many=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'position', 'foods')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class MenuSerializer(ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'audio_file_name', 'available', 'image', 'font_name', 'price', 'sections')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class ExtraSerializer(ModelSerializer):
    class Meta:
        model = Extra
        fields = ('id', 'name', 'type', 'price', 'discount_price')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class CompositionSerializer(ModelSerializer):
    selected_foods_list = FoodSerializer(many=True, required=False, source='selected_foods')
    extras_list = ExtraSerializer(many=True, required=False, source='extras')

    def create(self, validated_data):
        selected_foods = validated_data.pop('selected_foods')
        extras = validated_data.pop('extras') if validated_data.get('extras') else []
        composition = Composition.objects.create(menu_id=validated_data.get('menu'))

        extras_objs = Extra.objects.filter(id__in=extras)
        composition.extras.add(*extras_objs)

        composition_food_list = []
        for food in selected_foods:
            composition_food_list.append(CompositionFood(composition=composition, food_id=food))
        CompositionFood.objects.bulk_create(composition_food_list)
        return composition

    def run_validation(self, data=empty):
        super(CompositionSerializer, self).run_validation(data)
        return data

    class Meta:
        model = Composition
        fields = ('id', 'menu', 'selected_foods', 'extras', 'cost', 'extras_list', 'selected_foods_list')
        extra_kwargs = {
            'id': {'read_only': True, },
            'cost': {'read_only': True, },
        }


class OrderLineSerializer(ModelSerializer):
    composition = CompositionSerializer()

    def create(self, validated_data):
        composition_data = validated_data.pop('composition')
        composition_serializer = CompositionSerializer(data=composition_data)
        composition_serializer.is_valid(raise_exception=True)
        composition_serializer.save()
        composition = composition_serializer.data
        order_line = OrderLine.objects.create(composition_id=composition.get('id'), order=self.context.get('order'),
                                              **validated_data)

        return order_line

    def run_validation(self, data=empty):
        super(OrderLineSerializer, self).run_validation(data)
        return data

    class Meta:
        model = OrderLine
        fields = ('id', 'composition', 'quantity', 'order')
        extra_kwargs = {
            'id': {'read_only': True, },
            'order': {'read_only': True, }
        }


class OrderSerializer(ModelSerializer):
    lines = OrderLineSerializer(many=True)

    def create(self, validated_data):
        lines = validated_data.pop('lines') if validated_data.get('lines') else []
        order = super(OrderSerializer, self).create(validated_data)

        lines_serializer = OrderLineSerializer(data=lines, context={'order': order}, many=True)
        lines_serializer.is_valid(raise_exception=True)
        lines_serializer.save()
        lines = lines_serializer.data

        return order

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'number', 'status', 'client', 'lines')
        extra_kwargs = {
            'id': {'read_only': True, },
            'created_at': {'read_only': True, },
            'status': {'read_only': True, },
            'number': {'read_only': True, },
        }
