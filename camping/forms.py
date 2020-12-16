from django import forms
from .models import Profil
from .requetesSQL import (email_unique_verif, login, all_type_emplacement,
                          all_sevices)
from .scripts import date_18_years_before, date_1_week_after, free_dates_3mois

birthday_min = date_18_years_before()
date_resv_min = date_1_week_after()

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
                    error_messages =
                                {'unique': """Cet email existe déjà sur la
                                                base de données"""},
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

    def clean_telephone(self, *args, **kwargs):
        telephone = self.cleaned_data.get("telephone")
        if  not(1_000_000_000 > telephone > 100_000_000):
            raise forms.ValidationError("""Votre numéro de téléphone
                                           doit avoir 9 chiffres""")
        return telephone

    def clean_date_de_naissance(self, *args, **kwargs):
        date_de_naissance = self.cleaned_data.get("date_de_naissance")
        if date_de_naissance > birthday_min:
            raise forms.ValidationError("""Vous devez avoir au moins 18 ans pour
                                          vous enregister""")
        return date_de_naissance

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if email_unique_verif(email) == False:
            raise forms.ValidationError("""Cet email existe déjà sur la base de
                                     données""")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(label = '', widget = forms.TextInput(
                                                attrs={"class": "emailclass",
                                                "placeholder" : "Email"}))
    password = forms.CharField(label = '' , max_length = 30,
                    widget=forms.PasswordInput({'class': 'passwordclass',
                                                "placeholder" : "Password"}))


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email_unique_verif(email):
            raise forms.ValidationError("Cet email n'est pas enregistré")
        else:
            if login(email, password) == False :
                raise forms.ValidationError("Le mot de passe est incorrect")

class TypeEmplacementResa(forms.Form):
    liste = []
    options = tuple(all_type_emplacement())

    for i in range(len(options)):
       liste.append((options[i][0], options[i][0]))

    type_emplacement = forms.ChoiceField(label = '', choices = liste,
    widget=forms.Select(attrs={'class': 'check_type_service',}))

class ResaForm(forms.Form):
    nb_personnes = forms.IntegerField()
    def __init__(self, max, type_emplacement, qte, *args, **kwargs):
        super(ResaForm, self).__init__(*args, **kwargs)
        self.fields['nb_personnes'] = forms.IntegerField(label = 'Nombre des accompagnants',
                    widget = forms.NumberInput(attrs={"class": "nb_personnes",
                                        "placeholder" : "Nombre des personnes",
                                        "min" : 0,
                                        "max" : max}))

        services = all_sevices()
        services_liste = []
        for nom_service, description, prix in services:
           services_liste.append((nom_service, nom_service +' '+ prix))
        self.fields['options_locations'] = forms.ChoiceField( label = '',
        choices = services_liste, widget = forms.CheckboxSelectMultiple(
                                   attrs = {"class" : "options_locations"}))


        options = free_dates_3mois(type_emplacement, qte)
        liste = []
        for i in range(len(options)):
            liste.append((options[i], options[i]))

        self.fields['debut_sejour'] = forms.ChoiceField( label = '',
        choices = liste, widget = forms.Select(
                                            attrs = {"class" : "debut_sejour"}))

        self.fields['fin_sejour'] = forms.ChoiceField( label = '',
        choices = liste, widget = forms.Select(
                                            attrs = {"class" : "fin_sejour"}))


class PaymentForm(forms.Form):
    paiment_acompte = forms.BooleanField(widget = forms.CheckboxInput(
                                        attrs = {"class" : "payment"}))

class AccompagnantForm(forms.Form):
    nom_accomp = forms.CharField(max_length = 30, label = '',
                    widget = forms.TextInput(attrs={"class": "nom_accomp",
                                                "placeholder" : "Nom"}))
    prenom_accomp = forms.CharField(max_length = 30, label = '',
                    widget = forms.TextInput(attrs={"class": "prenom_accomp",
                                            "placeholder" : "Prenom"}))
    adresse = forms.CharField(max_length = 50, label = '',
                    widget = forms.TextInput(attrs={"class": "adresse",
                                            "placeholder" : "Adresse"}))

    telephone = forms.IntegerField(label = '',
                    widget = forms.NumberInput(attrs={"class": "telephone",
                                        "placeholder" : "Telephone"}))
    date_de_naissance = forms.DateField(label = '',
                    widget = forms.TextInput(attrs={"class": "date_naissance",
                                        "placeholder" : "Date de naissance",
                                        "type" : "date"}))

# class ReservationDateForm(forms.Form):
#     def __init__(self, type_emplacement, qte, *args, **kwargs):
#
#         options = free_dates_3mois(type_emplacement, qte)
#         liste = []
#         for i in range(len(options)):
#             liste.append((options[i], options[i]))
#
#         super(ReservationDateForm, self).__init__(*args, **kwargs)
#         self.fields['debut_sejour'] = forms.ChoiceField( label = '',
#         choices = liste, widget = forms.Select(
#                                             attrs = {"class" : "debut_sejour"}))
#
#         self.fields['fin_sejour'] = forms.ChoiceField( label = '',
#         choices = liste, widget = forms.Select(attrs = {"class" : "fin_sejour"}))
#
#     nb_persones = forms.IntegerField()
#
#     options = free_dates_6mois('Tente', 1)
#     liste = []
#
#     for i in range(len(options)):
#         liste.append((options[i], options[i]))
#     print(liste)
#
#     debut_sejour = forms.ChoiceField( label = '', choices = liste,
#         widget = forms.Select(
#             attrs = {"class" : "debut_sejour",
#                                         "placeholder" : "Date debut séjour"}))
#
#     fin_sejour = forms.ChoiceField( label = '', choices = liste,
#         widget = forms.Select(attrs = {"class" : "fin_sejour",
#                                         "placeholder" : "Date fin séjour"}))
