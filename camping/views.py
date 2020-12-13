from django.shortcuts import render, get_object_or_404, redirect
from .forms import  (ProfilForm, LoginForm, ReservationDateForm,
                        TypeEmplacementResa, NbPersonnesForm,
                        AccompagnantForm)
from datetime import date
from .requetesSQL import (login, reservation, search_id_profil,
                          insertion_base_info, all_sevices, personnes_max,
                          qte_emplacement)
from .scripts import generation_cle_aleatoire

id_profil = None
# insertion_base_info()

def login_create_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and login(form.data['email'],form.data['password']):
            global id_profil
            id_profil = search_id_profil(form.data['email'])
            return redirect("http://127.0.0.1:8000/profile/")
    context ={"form" : form }
    return render(request, "login.html", context)

def register_create_view(request):
    form = ProfilForm(request.POST or None)
    if form.is_valid():
        form.save()
        global id_profil
        id_profil = search_id_profil(form.data['email'])
        return redirect("http://127.0.0.1:8000/profile")
    context ={
        "form" : form
    }
    return render(request, "register.html", context)
# active_users = []
def home_create_view(request, *args, **kwargs):
    # if request.method == 'GET':
        # active_user.append(generation_cle_aleatoire())
    global cpt
    cpt = 0
    return render(request, "home.html", {})

def profile_create_view(request, *args, **kwargs):
    if id_profil :
        # obj = reservation(num_client)
        # print(obj)
        global cpt
        cpt = 0
        context = {"object" : 1}
        return render(request, "profile.html", context)
    else:
        return redirect("http://127.0.0.1:8000/login")



cpt = 0

info = {}
def reservation_create_view(request, *args, **kwargs):
    if id_profil :

        form1 = TypeEmplacementResa()


        nb_personnes = ()
        context = { "form1" : form1}
        global cpt
        global info

        if request.method == 'POST' and cpt == 0 :
            form1 = TypeEmplacementResa(request.POST)

            print(form1, form1.data.get('type_emplacement', False))
            type_emplacement = form1.data.get('type_emplacement', False)
            info["type_emplacement"] = type_emplacement
            personnes_maxi = personnes_max(type_emplacement)
            info["personnes_max"] = personnes_maxi
            form2 = NbPersonnesForm(personnes_maxi)
            context = {"form2" : form2}
            cpt += 1

        elif request.method == 'POST' and cpt == 1 :
            # nb_personnes = int(form2.data['nb_personnes'])
            # print(nb_personnes, personnes_maxi)
            # form2.clean(nb_personnes, personnes_maxi)
            # info["nb_personnes"] = nb_personnes
            # print("OK")
            nb_personnes = request.POST.get('nb_personnes')
            info['nb_personnes'] = int(nb_personnes)
            print(nb_personnes, 'ici')
            cpt += 1
            type_emplacement = info['type_emplacement']
            qte = qte_emplacement(type_emplacement)
            form3 = ReservationDateForm(type_emplacement, qte)
            context = {"form3" : form3}

        elif request.method == 'POST' and cpt == 2:
            info['debut_sejour'] = request.POST.get('debut_sejour')
            info['fin_sejour'] = request.POST.get('fin_sejour')
            accompagnantform = AccompagnantForm()
            nb_personnes = range(info['nb_personnes'])
            cpt += 1
            context = {"form4" : accompagnantform, "nb_personnes" : nb_personnes}
        elif request.method == 'POST' and cpt == 3:
            nom = request.POST.get('nom_client')
            print(nom) 
        return render(request, "reservation.html", context)
    else :
        return redirect("http://127.0.0.1:8000/login")

def services_create_view(request, *args, **kwargs):
    services = all_sevices()
    range1   = range(len(services))
    context = { "services" : services }
    return render(request, "services.html", context)
