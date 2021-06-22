from django import forms

from .models import Adress


class AddressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = [
            'address_line_1', 'address_line_2',
            'city', 'country', 'state', 'postal_code'
        ]
