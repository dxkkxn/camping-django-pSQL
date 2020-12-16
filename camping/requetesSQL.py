import psycopg2
import datetime

datenow = datetime.date.today()
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

premier_samedi_sept = first_samedi_sept()
dernier_samedi_juin = last_samedi_juin()

def insertion_base_info():
    request_sql = """INSERT INTO services_proposes
    (nom_service, description, prix_suplement) VALUES (%s, %s, %s)"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")

    cur = conn.cursor()

    cur.execute(request_sql,("Laverie",
    """Ce service est ouvert tous les jours de 8h à 20h.
    Une salle contenant 20 machines à laver est mise à disposition
    aux clients y adhérant.""", 15))



    cur.execute(request_sql, ("Demi-Pension",
    """Ce service est mis à disposition tous les jours aux
    plages horaires suivants:

    - 11h30 / 14h30
    - 18h30 / 21h30

    Vous pourrez choisir parmis une variété de 4 plats quotidiens (dont 1 plat
    végétarien/végan).  tout en bénéficiant d'une entrée et d'un déssert
    au choix.""", 7))


    cur.execute(request_sql, ("Parc aquatique",
    """Ce service est ouvert tous les Lundi, Mercredi, Vendredi et Dimanche,
     de 10h à 19h. Divers jeux aquatiques sont mis à disposition :
     toboggans, piscine à vagues, ... """, 12))

    request_sql = """ INSERT INTO type_emplacement VALUES (%s, %s, %s)"""
    cur.execute(request_sql, ("Tente", 6, 20))
    cur.execute(request_sql, ("CampingCar", 6, 40))
    cur.execute(request_sql, ("Mobilehome pétit", 6, 60))
    cur.execute(request_sql, ("Mobilehome grand", 8, 80))
    cur.execute(request_sql, ("Chalets", 10, 100))

    request_sql = """INSERT INTO emplacement (type_emplacement) VALUES (%s) """
    for i in range(3):
        cur.execute(request_sql, ("Tente",))
        cur.execute(request_sql, ("CampingCar",))
        cur.execute(request_sql, ("Mobilehome pétit",))
        cur.execute(request_sql, ("Mobilehome grand",))
        cur.execute(request_sql, ("Chalets",))

    request_sql = """INSERT INTO option_location VALUES (%s, %s) """
    cur.execute(request_sql, ("Mois", 20))
    cur.execute(request_sql, ("Jour", 0))
    cur.execute(request_sql, ("Semaine", 10))

    request_sql = """INSERT INTO saison (libelle_saison, date_com, date_fin,
    coef_majoration) VALUES (%s, %s, %s, %s)"""
    cur.execute(request_sql, ("haut saison", dernier_samedi_juin,
                              premier_samedi_sept, 20))

    cur.execute(request_sql, ("bas saison", premier_samedi_sept, '2020-12-31'
                              ,0))
    request_sql = """INSERT INTO fidelite VALUES (%s, %s)"""
    cur.execute(request_sql, (0,0))

    print("information sur la base")
    conn.commit()
    cur.close()
    conn.close()

def all_sevices():
    request_sql = """SELECT nom_service, description,
                     concat( prix_suplement, ' euros/jour')
                     FROM services_proposes"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql)
    obj = cur.fetchall()
    cur.close()
    conn.close()
    return obj

def login(email, password):
    request_sql = """SELECT email, password FROM profil WHERE email = %s
                    AND password = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(email, password))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    if obj == None :
        return False
    else:
        return True

def reservation(id_profil):
    request_sql = """SELECT * FROM responsable NATURAL JOIN reservation
                     WHERE id_profil = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(id_profil,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj

def email_unique_verif(email):  # Returns True if email doesn´t exist
    request_sql = "SELECT email FROM profil where email = %s"
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(email,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    if obj == None:
        return True
    else :
        return False

def search_id_profil(email):
    request_sql = """SELECT id_profil FROM profil WHERE email = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(email,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj[0]

def days_reservation_free(type_emplacement):
    request_sql = """SELECT  debut_sejour, fin_sejour FROM reservation
                    where type_emplacement = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (type_emplacement,))
    dates = cur.fetchall()
    # gestion des dates
    cur.close()
    conn.close()
    return None

def all_type_emplacement():
    request_sql = """SELECT type_emplacement, count(num_emplacement)
                    FROM emplacement GROUP BY type_emplacement"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql)
    obj = cur.fetchall()
    cur.close()
    conn.close()
    return obj

def qte_emplacement(type_emplacement):
    request_sql = """SELECT count(num_emplacement)
                    FROM emplacement WHERE type_emplacement = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (type_emplacement,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj[0]

def personnes_max(type_emplacement) :
    request_sql = """SELECT nb_personnes_max FROM type_emplacement
                     WHERE type_emplacement = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (type_emplacement,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj[0]

def occuped_dates(type_emplacement):
    request_sql = """SELECT (debut_sejour) FROM reservation
                     WHERE type_emplacement = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (type_emplacement,))
    obj = cur.fetchall()

    request_sql = """SELECT (fin_sejour) FROM reservation
                     WHERE type_emplacement = %s """
    cur.execute(request_sql, (type_emplacement,))
    obj1 = cur.fetchall()
    liste = []
    for i in range(len(obj)):
        liste.append((obj[i][0], obj1[i][0]))

    cur.close()
    conn.close()

    return liste

def prix_emplacement(type_emplacement):
    request_sql = """SELECT prix_journee FROM type_emplacement
                     WHERE type_emplacement = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (type_emplacement,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj[0]

def remise_option(option_location):
    request_sql = """SELECT remise_option FROM option_location
                     WHERE option_location = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql, (option_location,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    return obj[0]

def saisons():
    request_sql = """SELECT (date_com) FROM saison """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql)
    obj = cur.fetchall()

    request_sql = """SELECT (date_fin) FROM saison """
    cur.execute(request_sql)
    obj1 = cur.fetchall()

    request_sql = "SELECT coef_majoration FROM saison"
    cur.execute(request_sql)
    coef = cur.fetchall()

    request_sql = "SELECT code_saison FROM saison"
    cur.execute(request_sql)
    saison = cur.fetchall()

    liste = []
    for i in range(len(obj)):
        liste.append((saison[i][0], obj[i][0], obj1[i][0], coef[i][0]))
    cur.close()
    conn.close()
    return liste

def remise_fidelite(id_profil):
    request_sql = """SELECT point_fidelite, reduc_fidelite
                     FROM responsable NATURAL JOIN fidelite
                     WHERE id_profil = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(id_profil,))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    if obj == None:
        return (0, 0)
    else :
        return obj

def prix_service(service):
    request_sql = """SELECT prix_suplement
                     FROM services_proposes
                     WHERE nom_service = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(service,))
    obj = cur.fetchone()[0]
    cur.close()
    conn.close()
    return obj

def insertion(dico):
    request_sql = """SELECT MAX(num_reservation)
                     FROM reservation"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()

    cur.execute(request_sql)
    obj = cur.fetchone()[0]
    if obj == None:
        pk = 0
    else:
        pk = obj + 1

    request_sql = """INSERT INTO reservation (num_reservation, nb_personnes,
    acompte,reglement, reglement_bool, date_reservation, debut_sejour,
    fin_sejour, annulation, presence, code_saison, option_location,
    type_emplacement) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""




    cur.execute(request_sql,(pk, dico['nb_personnes'], dico['acompte'],
                            dico['reglement'], False, dico['date_reservation'],
                            dico['debut_sejour'], dico['fin_sejour'], False,
                            False, dico['code'], dico['option'],
                            dico['type_emplacement']))


    request_sql = """INSERT INTO reservation_services (num_reservation,
                    nom_service) VALUES (%s, %s)"""
    for service in dico['services']:
        cur.execute(request_sql, (pk, service))

    request_sql = """INSERT INTO client (nom_client, prenom_client, adresse,
                    telephone, date_de_naissance, num_reservation) VALUES
                    (%s, %s, %s, %s, %s, %s)"""
    if dico.get('nom_accomp'):
        i = 0
        n = len(dico['nom_accomp'])
        nom_accomp = dico['nom_accomp']
        prenom_accomp = dico['prenom_accomp']
        adresse = dico['adresse']
        telephone = dico['telephone']
        date_de_naissance = dico['date_de_naissance']
        while i < n:
            cur.execute(request_sql,(nom_accomp[i],
            prenom_accomp[i], adresse[i], telephone[i], date_de_naissance[i],
            pk))
            conn.commit()
            i += 1

    request_sql = """SELECT * FROM profil WHERE id_profil = %s"""
    cur.execute(request_sql, (dico['id_profil'],))
    donnees = cur.fetchall()[0]

    request_sql = """SELECT MAX(num_client) FROM client"""
    cur.execute(request_sql)
    num_client = cur.fetchone()[0]
    print(num_client)
    if num_client == None:
        num_client = 0
    else:
        num_client += 1

    request_sql = """INSERT INTO client (num_client, nom_client, prenom_client,
     adresse, telephone, date_de_naissance, num_reservation) VALUES
     (%s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(request_sql, (num_client, donnees[1], donnees[2], donnees[3],
                             donnees[4], donnees[5], pk))

    request_sql = """SELECT * FROM responsable WHERE email = %s"""

    cur.execute(request_sql, (donnees[6],))

    print(cur.fetchone(), dico['id_profil'])
    print(donnees)
    if cur.fetchone() == None:
        request_sql = """ INSERT INTO responsable (email, password,
        id_profil, num_client, num_reservation, point_fidelite) VALUES (%s, %s,
        %s, %s, %s, %s)"""
        cur.execute(request_sql, (donnees[6], donnees[7], dico['id_profil'],
                    num_client, pk, dico['fidelite']))

    conn.commit()
    cur.close()
    conn.close()

def delete_resv(num_reservation):
    request_sql = """ DELETE FROM reservation CASCADE WHERE num_reservation = %s """
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(num_reservation,))
    conn.commit()
    cur.close()
    conn.close()
    return True

# print(login("youssef@benjelloun.com","1234"))
# Execute a command: this creates a new table
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
#
# # Pass data to fill a query placeholders and let Psycopg perform
# # the correct conversion (no more SQL injections!)
# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
# ...      (100, "abc'def"))
#
# # Query the database and obtain data as Python objects
# >>> cur.execute("SELECT * FROM test;")
# >>> cur.fetchone()
# (1, 100, "abc'def")
#
# # Make the changes to the database persistent
# conn.commit()
#
#
# cur.close()
# conn.close()
