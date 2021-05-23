from rest_framework.serializers import ModelSerializer

from mainapp.models import Client, PhoneNumber, Address, Menu, Section, Food, Extra, Composition, OrderLine, Order


class PhoneSerializer(ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'client', 'phone')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'client', 'address')
        extra_kwargs = {
            'id': {'read_only': True, }
        }


class ClientSerializer(ModelSerializer):
    phones = PhoneSerializer(many=True, required=False)
    address = AddressSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'address', 'phone', 'email', 'phones', 'addresses')
        extra_kwargs = {
            'id': {'read_only': True, }
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
        models = Menu
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
    selected_foods = FoodSerializer(many=True)
    extras = ExtraSerializer(many=True, required=False)

    class Meta:
        model = Composition
        fields = ('id', 'menu', 'selected_foods', 'extras', 'cost')
        extra_kwargs = {
            'id': {'read_only': True, },
            'cost': {'read_only': True, }
        }


class OrderLineSerializer(ModelSerializer):
    composition = CompositionSerializer(many=True)

    class Meta:
        model = OrderLine
        fields = ('id', 'composition', 'quantity', 'order')
        extra_kwargs = {
            'id': {'read_only': True, },
            'order': {'read_only': True, }
        }


class OrderSerializer(ModelSerializer):
    lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'number', 'status', 'client', 'lines')
        extra_kwargs = {
            'id': {'read_only': True, },
            'created_at': {'read_only': True, },
            'status': {'read_only': True, },
            'number': {'read_only': True, },
        }
