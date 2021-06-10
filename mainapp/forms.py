from crispy_forms.helper import FormHelper
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from mainapp.models import Menu, Section, Food, Extra, Order, OrderLine


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "palceholder": _('Username')
    }), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": _('Password')
    }), required=True)

    @property
    def get_username(self):
        return self.cleaned_data.get('username', "")

    @property
    def get_password(self):
        return self.cleaned_data.get('password', "")


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('name', 'image', 'price', 'available', 'audio_file_name', 'font_name')


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'position', 'menu')


MenuWithSectionsFormSet = inlineformset_factory(Menu, Section, fields=('name', 'position',),
                                                extra=0, min_num=1, validate_min=True, max_num=3,
                                                validate_max=True)


class SectionsFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SectionsFormsetHelper, self).__init__(*args, **kwargs)
        self.template = 'bootstrap4/table_inline_formset.html'


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'description', 'image', 'price', 'discount_price', 'section')


class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields = ('name', 'type', 'image', 'price', 'discount_price')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('composition', 'quantity')



class DeleteForm(forms.Form):
    pass
