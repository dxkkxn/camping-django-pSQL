import psycopg2
# from .scripts import first_samedi_sept, last_samedi_juin
# premier_samedi_sept = first_samedi_sept()
# dernier_samedi_juin = last_samedi_juin()

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
        cur.execute(request_sql, ("Mobilehome_p",))
        cur.execute(request_sql, ("Mobilehome_g",))
        cur.execute(request_sql, ("Chalets",))

    request_sql = """INSERT INTO option_location VALUES (%s, %s) """
    cur.execute(request_sql, ("Mois", 20))
    cur.execute(request_sql, ("Jour", 0))
    cur.execute(request_sql, ("Semaine", 10))

    request_sql = """INSERT INTO saison (libelle_saison, date_com, date_fin,
    coef_majoration) VALUES (%s, %s, %s, %s)"""
    cur.execute(request_sql, ("haut saison", dernier_samedi_juin,
                              premier_samedi_sept, 20))
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

def reservation(num_client):
    request_sql = """SELECT * FROM client NATURAL JOIN reservation
                    NATURAL JOIN client WHERE num_client = %s"""
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute(request_sql,(num_client,))
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
