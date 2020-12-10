from django import forms
from .models import Profil

class ProfilForm(forms.ModelForm):
    nom_client = forms.CharField(max_length = 30, label = '',
                    widget = forms.TextInput(attrs={"class": "nom-client",
                                                "placeholder" : "Nom"}))
    prenom_client = forms.CharField(max_length = 30, label = '',
                    widget = forms.TextInput(attrs={"class": "prenom-client",
                                            "placeholder" : "Prenom"}))
    adresse = forms.CharField(max_length = 50, label = '',
                    widget = forms.TextInput(attrs={"class": "adresse",
                                            "placeholder" : "Adresse"}))

    telephone = forms.IntegerField(label = '',
                    widget = forms.NumberInput(attrs={"class": "telephone",
                                        "placeholder" : "Telephone"}))
    date_de_naissance = forms.DateField(label = '',
                    widget = forms.TextInput(attrs={"class": "date-naissance",
                                        "placeholder" : "Date de naissance",
                                        "type" : "date"}))
    email = forms.EmailField(label = '',
                    widget = forms.TextInput(attrs={"class": "adresse",
                                            "placeholder" : "Email"}))
    password = forms.CharField(max_length = 30, label = '',
                                 widget=forms.PasswordInput(
                                 attrs={"class": "mdp",
                                    "placeholder" : "Mot de passe"}))
    class Meta:
        model = Profil
        fields = ["nom_client", "prenom_client","adresse",
                  "telephone", "date_de_naissance", "email", "password"]
    # def test(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     if "@gmail" in email:
    #         raise forms.ValidationError("pas de gmail chez nous")
    #     return email
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if "@gmail" in email:
            raise forms.ValidationError("pas de gmail chez nous")
        return email



class LoginForm(forms.Form):
    email = forms.EmailField(label = '', widget = forms.TextInput(
                                                attrs={"class": "emailclass",
                                                "placeholder" : "Email"}))
    password = forms.CharField(label = '' , max_length = 30,
                    widget=forms.PasswordInput({'class': 'passwordclass',
                                                "placeholder" : "Password"}))
# class Reservation(forms.From):
