from django.shortcuts import render, get_object_or_404, redirect
from .forms import  ClientForm, LoginForm
from datetime import date
from .requetesSQL import login
from .scripts import generation_cle_aleatoire
from django import forms

# from .requetesSQL import login
# Create your views here.

def login_create_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if login(form.data['email'],form.data['password']):
            return redirect("http://127.0.0.1:8000")
        else:
            raise forms.ValidationError("Le mot de passe ou l'email sont incorrects")
    context ={"form" : form }
    return render(request, "login.html", context)

def client_create_view(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except:
            raise forms.ValidationError("Le mot de passe ou l'email sont incorrects")
        print(form.data['date_de_naissance'], type(form.data['date_de_naissance']))
        return redirect("http://127.0.0.1:8000")
    context ={
        "form" : form
    }
    return render(request, "register.html", context)
# active_users = []
def home_create_view(request, *args, **kwargs):
    # if request.method == 'GET':
        # active_user.append(generation_cle_aleatoire())
    return render(request, "home.html", {})

# def clean_presentation_date(self, value):
#     if value >=  and value < date.today():
#         raise form.ValidationError('The date must be ...')
# return value
