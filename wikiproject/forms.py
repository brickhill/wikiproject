from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User




class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email address",
    )

    class Meta:
        model = User
        fields = ("username", "email")


class ContactForm(forms.Form):

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6
            }
        )
    )
