from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import *


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    age = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        return age


class CustomerRegistrationForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'review', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }