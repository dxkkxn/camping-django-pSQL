import random
import datetime
from .requetesSQL import (occuped_dates, prix_emplacement, remise_option,
                          saisons, remise_fidelite, prix_service)


def generation_cle_aleatoire():
    return random.getrandbits(64)

datenow = datetime.date.today()

def date_18_years_before():
    return datenow - datetime.timedelta(days=(18*365.25))

def date_1_week_after():
    return datenow + datetime.timedelta(days=(7))


def calcul_reglement_acompte(id_profil, type_emplacement, debut_sejour,
    fin_sejour, services):
    prix = prix_emplacement(type_emplacement)
    debut_sejour = datetime.datetime.strptime(debut_sejour, '%Y-%m-%d')
    fin_sejour   = datetime.datetime.strptime(fin_sejour, '%Y-%m-%d')
    debut_sejour = datetime.datetime.date(debut_sejour)
    fin_sejour   = datetime.datetime.date(fin_sejour)
    diff = fin_sejour - debut_sejour

    if diff.days > 30 :
        remise = remise_option('Mois')
        option = 'Mois'
    elif diff.days > 7 :
        remise = remise_option('Semaine')
        option = 'Semaine'
    else:
        remise = remise_option('Jour')
        option = 'Jour'

    saison = saisons()
    coef_def = 0
    for code, date_com, date_fin, coef in saison:
        if date_com < debut_sejour < date_fin:
            coef_def = coef
            code_saison = code

    chosen_services = services
    for service in chosen_services:
        prix += prix_service(service)

    fidelite = remise_fidelite(id_profil)
    remise = coef_def + remise + fidelite[1]
    total = diff.days * float(prix)
    major = coef_def/100 * total
    total = total + major
    remise = (remise/100) * total
    total = total - remise
    acompte = 0.10 * total

    return (datenow, total, acompte, fidelite[0], option, code)

def free_dates_3mois(type_emplacement, qte):
    dates = []
    date_min_resa = date_1_week_after()
    for i in range(1, 3*30):
        date = date_min_resa + datetime.timedelta(days = i)
        dates.append(date)

    occup_dates = occuped_dates(type_emplacement)
    dico_dates = {}
    for date in occup_dates:
        if date[0] in dates:
            sup_date = date[0]
            i = 1
            while sup_date <= date[1]:
                if dico_dates.get(sup_date):
                    dico_dates[sup_date] += 1
                else :
                    dico_dates[sup_date] = 1
                sup_date = sup_date + datetime.timedelta(days = 1)
                i += 1

    for key, value in dico_dates.items() :
        if value >= qte:
            dates.remove(key)

    return dates
