import random
import datetime
def generation_cle_aleatoire():
    return random.getrandbits(64)

datenow = datetime.date.today()
def date_18_years_before():
    return datenow - datetime.timedelta(days=(18*365.25))
print(date_18_years_before())
