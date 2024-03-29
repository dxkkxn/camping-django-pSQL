from django.shortcuts import render, get_object_or_404, redirect
from .forms import  (ProfilForm, LoginForm, TypeEmplacementResa, ResaForm,
                        AccompagnantForm, PaymentForm, EmailForm)
from datetime import date
from .requetesSQL import (login, reservation, search_id_profil,
                          insertion_base_info, all_sevices, personnes_max,
                          qte_emplacement, insertion, delete_resv, admin,
                          ajout_admin, personnes_camping, donnees_resv, 
                          emplacement_plus_resv)
from .scripts import calcul_reglement_acompte, acompte

id_profil = None
#insertion_base_info()

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
    global index
    global info
    global id_profil
    cpt = 0
    index = 0
    info = {}

    if request.method == 'POST':
        id_profil = None
    context = { 'profil' : id_profil }
    return render(request, "home.html", context )

def profile_create_view(request, *args, **kwargs):
    if id_profil :
        # obj = reservation(num_client)
        # print(obj)
        global cpt
        global info
        info = {}
        cpt = 0
        context = {}
        resv = reservation(id_profil)
        print(id_profil)
        print(resv)
        if resv != None:
            date_res = resv[11]
            date_fin = resv[12]
            print(resv)
            context = {"object" : resv, "date_res" : date_res,
                   "date_fin" : date_fin}

        return render(request, "profile.html", context)

    else:
        return redirect("http://127.0.0.1:8000/login")

def resv_annulation_view(request, *args, **kwargs):
    if id_profil:
        resv = reservation(id_profil)
        acc = acompte(resv[11])
        print(resv)
        context = { 'acompte' : acc }
        if request.method == 'POST':
            delete_resv(resv[0])
            print('OK')
            return redirect ("http://127.0.0.1:8000/profile/")
        return render(request, "reservation_annulation.html", context)
    return redirect("http://127.0.0.1:8000/login/")

cpt = 0
index = 0
info = {}
def reservation_create_view(request, *args, **kwargs):
    if id_profil and not(reservation(id_profil)) :
        form1 = TypeEmplacementResa()
        nb_personnes = ()
        context = { "form1" : form1}
        global cpt
        global info
        global index
        if request.method == 'POST' and cpt == 0 :
            form1 = TypeEmplacementResa(request.POST)

            type_emplacement = form1.data.get('type_emplacement', False)
            info["type_emplacement"] = type_emplacement

            personnes_maxi = personnes_max(type_emplacement)
            info["personnes_max"] = personnes_maxi

            qte = qte_emplacement(type_emplacement)
            form2 = ResaForm(personnes_maxi, type_emplacement, qte)
            context = {"form2" : form2}
            cpt += 1

        elif request.method == 'POST' and cpt == 1 :
            nb_personnes = request.POST.get('nb_personnes')
            options_locations = request.POST.getlist('options_locations')

            info['nb_personnes'] = int(nb_personnes)
            info['services'] = options_locations
            info['debut_sejour'] = request.POST.get('debut_sejour')
            info['fin_sejour'] = request.POST.get('fin_sejour')

            if int(nb_personnes) == 0:
                (date_reservation, reglement, acompte, ptsfidelite,
                option, code) = calcul_reglement_acompte(
                id_profil, info['type_emplacement'], info['debut_sejour'],
                        info['fin_sejour'], info['services'])
                info['id_profil'] = id_profil
                info['date_reservation'] = date_reservation
                info['reglement'] = reglement
                info['acompte']  =  acompte
                info['fidelite'] = ptsfidelite
                info['option'] = option
                info['code'] = code
                print(info)
                form5 = PaymentForm()
                context = {'reglement' : reglement, 'acompte' : acompte,
                           'form5': form5 }
                cpt += 2
                print(cpt)
            else:
                i = index + 1
                form3 = AccompagnantForm()
                context = {"form3" : form3, "i" : i}
                cpt += 1

        elif request.method == 'POST' and cpt == 2 :
            nb_personnes = info['nb_personnes']

            if index < nb_personnes:

                nom = request.POST.get('nom_accomp')
                prenom = request.POST.get('prenom_accomp')
                adresse = request.POST.get('adresse')
                telephone = request.POST.get('telephone')
                date_de_naissance = request.POST.get('date_de_naissance')

                if info.get('nom_accomp'):
                    info['nom_accomp'].append(nom)
                else:
                    info['nom_accomp'] = [nom]

                if info.get('prenom_accomp'):
                    info['prenom_accomp'].append(prenom)
                else:
                    info['prenom_accomp'] = [prenom]

                if info.get('adresse'):
                    info['adresse'].append(adresse)
                else:
                    info['adresse'] = [adresse]

                if info.get('telephone'):
                    info['telephone'].append(telephone)
                else:
                    info['telephone'] = [telephone]

                if info.get('date_de_naissance'):
                    info['date_de_naissance'].append(date_de_naissance)
                else:
                    info['date_de_naissance'] = [date_de_naissance]

                if index == nb_personnes - 1 :
                    (date_reservation, reglement, acompte, ptsfidelite,
                    option, code) = calcul_reglement_acompte(
                    id_profil, info['type_emplacement'], info['debut_sejour'],
                            info['fin_sejour'], info['services'])
                    info['id_profil'] = id_profil
                    info['date_reservation'] = date_reservation
                    info['reglement'] = reglement
                    info['acompte']  =  acompte
                    info['fidelite'] = ptsfidelite
                    info['option'] = option
                    info['code'] = code
                    print(info)
                    form5 = PaymentForm()
                    context = {'reglement' : reglement, 'acompte' : acompte,
                               'form5': form5 }
                    cpt += 1

                else:
                    i = index + 2
                    accompagnantform = AccompagnantForm()
                    context = {"form4" : accompagnantform, "i" : i}
                index += 1
        elif request.method == 'POST' and cpt == 3 :
            print('ok')
            if request.POST.get('paiment_acompte') == 'on':
                insertion(info)
                print('insertion ok')
                return redirect("http://127.0.0.1:8000/profile/")

        return render(request, "reservation.html", context)
    else :
        return redirect("http://127.0.0.1:8000/profile")

def services_create_view(request, *args, **kwargs):
    services = all_sevices()
    range1   = range(len(services))
    context = { "services" : services }
    return render(request, "services.html", context)

def login_admin_create_view (request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        log = login(form.data['email'],form.data['password'])
        print(admin(form.data['email']))
        if form.is_valid() and log and admin(form.data['email']) :
            global id_profil
            id_profil = form.data['email']
            return redirect('http://127.0.0.1:8000/camping/admin')
    context = { 'form' : form }
    return render(request, 'login_admin.html', context)

def admin_create_view(request):
    global id_profil
    context = {}
    if id_profil and admin(id_profil):
        if request.POST.get('ajout'):
            form = EmailForm
            context = { "form" : form }
        if request.POST.get('valider'):
            form = EmailForm(request.POST)
            if form.is_valid():
                ajout_admin(form.data['email'])
                context = {"ok" : "OPERATION REUSSI"}
            else:
                context = { "form" : form }
        if request.POST.get('per'):
            personnes = personnes_camping()
            if personnes == None:
                personnes = 0
            context = { "personnes" : personnes }
        if request.POST.get('deco'):
            id_profil = None
            return redirect ('http://127.0.0.1:8000/')
        if request.POST.get('historique'):
            historique = donnees_resv()
            context = {'historique': historique}
        
        if request.POST.get('plusempl'):
            print ('OK')
            empl = emplacement_plus_resv()
            print(empl)
            context = { 'empl' : empl }
            
        return render(request, 'admin.html', context)

        
    else:
        return redirect('http://127.0.0.1:8000/')
