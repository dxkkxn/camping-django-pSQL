import random
import datetime
from .requetesSQL import occuped_dates

def generation_cle_aleatoire():
    return random.getrandbits(64)

datenow = datetime.date.today()

def date_18_years_before():
    return datenow - datetime.timedelta(days=(18*365.25))

def date_1_week_after():
    return datenow + datetime.timedelta(days=(7))

def last_samedi_juin():
    current_year = datenow.year
    for i in range(1,31):
        june_days = datetime.date(current_year, 6, i)
        if june_days.weekday() == 5:
            last_samedi = june_days
    return last_samedi

def first_samedi_sept():
    current_year = datenow.year
    for i in range(1,31):
        sept_days = datetime.date(current_year, 9, i)
        if sept_days.weekday() == 5:
            return sept_days
    return -1

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

print(free_dates_3mois("Tente", 1))
