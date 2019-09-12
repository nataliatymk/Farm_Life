from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget


from farmlife.models import AgriculturalLand, AgriculturalMachinery, Plants, AdditionalIncome, ExtraExpenses


class LoginForm (forms.Form):
    username = forms.CharField (label="Login")
    password = forms.CharField (label="Hasło", widget=forms.PasswordInput)


class LandForm (forms.ModelForm):
    class Meta:
        model = AgriculturalLand
        exclude = ['user_log']
        labels = {"land_name": "Nazwa", "type": "Typ", "area": "Powierzchnia (ha)", "comments": "Komentarz"}


class MachineryForm (forms.ModelForm):
    def __init__ (self, *args, user_log=None, **kwargs):
        super ().__init__ (*args, **kwargs)
        self.fields['land_machinery'].queryset = AgriculturalLand.objects.filter (user_log=user_log)
    class Meta:
        model = AgriculturalMachinery
        exclude = ['user_log']
        widgets = {"land_machinery":forms.CheckboxSelectMultiple(), "time_add": forms.SelectDateWidget}
        labels = {"machinery_name":"Nazwa maszyny", "fuel_consumption": "Spalanie (l/100km)", "land_machinery":"Wyjazd na pole",
                  "accessories":"Dodatkowy sprzęt", "accessories_width":"Szerokość dodatku (m)", "time_add":"Data użytkowania" }



class PlantForm (forms.ModelForm):
    def __init__ (self, *args, user_log=None, **kwargs):
        super ().__init__ (*args, **kwargs)
        self.fields['land_plant'].queryset = AgriculturalLand.objects.filter (user_log=user_log)
    class Meta:
        model = Plants
        exclude = ['user_log']
        widgets = {"land_plant": forms.CheckboxSelectMultiple (), "time_add": forms.SelectDateWidget}
        labels = {"plant_name": "Nazwa rośliny", "expected_yield": "Przewidywany plon (t)",
                  "plant_price": "Cena nasion (zł)", "harvest": "Zbiór (t)",
                  "sale": "Cena sprzedaży (zł/t)", "land_plant": "Obsadzone pole", "comments": "Komentarz", "time_add":"Data zbioru"}


class IncomeForm (forms.ModelForm):
    class Meta:
        model = AdditionalIncome
        exclude = ['user_log']
        widgets = {"time_add": forms.SelectDateWidget}
        labels = {"income_name": "Nazwa", "cost": "Koszt", "time_add":"Data"}


class ExpensesForm (forms.ModelForm):
    class Meta:
        model = ExtraExpenses
        exclude = ['user_log']
        widgets = {"time_add": forms.SelectDateWidget}
        labels = {"expenses_name": "Nazwa", "cost": "Koszt", "time_add":"Data"}


class UserForm (forms.Form):
    username = forms.CharField (label="Login")
    email = forms.CharField (label="E-mail")
    password = forms.CharField (label="Hasło", widget=forms.PasswordInput)
    check_password = forms.CharField (label="Powtórz hasło", widget=forms.PasswordInput)

    def clean (self):
        cleaned_data = super ().clean ()
        password = cleaned_data.get ("password")
        check_password = cleaned_data.get ("check_password")

        if password != check_password:
            raise forms.ValidationError ("Błędne hasło")


class BalanceForm (forms.Form):
    fuel_price = forms.DecimalField(max_digits=4, decimal_places=2, label="Cena paliwa")
    start_date = forms.DateField(widget=AdminDateWidget, label="Data startowa")
    end_date = forms.DateField (widget=AdminDateWidget, label="Data końcowa")

class EditUserForm (forms.Form):
    password = forms.CharField (label="Hasło", widget=forms.PasswordInput)
    check_password = forms.CharField (label="Powtórz hasło", widget=forms.PasswordInput)

    def clean (self):
        cleaned_data = super ().clean ()
        password = cleaned_data.get ("password")
        check_password = cleaned_data.get ("check_password")

        if password != check_password:
            raise forms.ValidationError ("Błędne hasło")