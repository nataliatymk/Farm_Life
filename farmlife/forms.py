from django import forms
from django.forms import ModelForm

from farmlife.models import AgriculturalLand, LANDS


class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

class LandForm(forms.ModelForm):
    class Meta:
        model = AgriculturalLand
        fields= "__all__"
        labels = {"land_name": "Nazwa", "type": "Typ", "area": "Powierzchnia (ha)", "comments": "Komentarz"}

