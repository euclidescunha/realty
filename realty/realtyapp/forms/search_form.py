from django import forms

class SearchForm(forms.Form):
    address = forms.CharField(max_length=200)
    search_nearby = forms.BooleanField(required=False)
