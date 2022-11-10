from django import forms
from .models import *



class VendorForms(forms.ModelForm):
    class Meta:
        model=Vendor
        fields=['vendor_name','vendor_license']