from .models import *
from django import forms


class UserForms(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','phone_number','password','confirm_password']


    def clean(self):
        cleaned_data=super(UserForms,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        print(password)
        print(confirm_password)                
        if password!=confirm_password:
            raise forms.ValidationError('Password doesnot match')