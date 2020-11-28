import psycopg2

def login(user, password):
    conn = psycopg2.connect( host = "localhost",
                            database = "Camping",
                            user = "postgres",
                            password = "postgres")
    cur = conn.cursor()
    cur.execute("SELECT email, password FROM camping_client WHERE email = %s AND password = %s",
                (user, password))
    obj = cur.fetchone()
    cur.close()
    conn.close()
    if obj != None :
        return True
    else:
        return False
        
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
