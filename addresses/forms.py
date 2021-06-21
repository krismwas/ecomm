from django import forms

from .models import Adress


class AddressForm(forms.ModelForm):
    class Meta:
        model = Adress
