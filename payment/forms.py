from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre completo'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electronico'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primer nombre'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Segundo nombre'}), required=True)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Provincia'}), required=False)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codigo Postal'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pais'}), required=True)
    
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_emails', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
        
        exclude = ['user',]