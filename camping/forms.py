from django import forms
from .models import Client
import psycopg2

class ClientForm(forms.ModelForm):
    nom_client = forms.CharField(max_length = 30)
    prenom_client = forms.CharField(max_length = 30)
    adresse = forms.CharField(max_length = 50)
    telephone = forms.IntegerField() #MinimumLengthValidator = 9
    date_de_naissance = forms.DateField()#
    email = forms.EmailField(label = 'Votre email')
    password = forms.CharField(max_length = 30,
                                 widget=forms.PasswordInput())
    class Meta:
        model = Client
        fields = ["num_client","nom_client", "prenom_client","adresse",
                  "telephone", "date_de_naissance", "email", "password"]



class LoginForm(forms.Form):
    email = forms.EmailField(label = '', widget = forms.TextInput(
                                                attrs={"class": "emailclass",
                                                "placeholder" : "Email"}))
    password = forms.CharField(label = '' , max_length = 30,
                            widget=forms.PasswordInput({'class': 'passwordclass',
                                                        "placeholder" : "Password"}))
