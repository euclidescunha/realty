from django import forms

from realtyapp.models import Realty

class RealtyForm(forms.ModelForm):

    class Meta:
        model = Realty
        fields = ('address', 'photo')