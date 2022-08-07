# Import the required module
import pymysql

conn = None

# establish a connection
def connect():
    global conn
    # select database
    conn = pymysql.connect(host="localhost", user="root", password="root", db="moviesDB", cursorclass=pymysql.cursors.DictCursor)


def get_films_cursor():
    # connect
    if (not conn):
        connect()

    query1 = "select film.filmname, actor.actorname from film join filmcast on film.filmid = filmcast.castfilmid join actor on filmcast.castactorid = actor.actorid order by filmname asc, actorname asc;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query1)
        return cursor


def actors_dob_gen(dob, gender):
    # connect
    if (not conn):
        connect()

    query2 = "select actorname, monthname(actordob) as month, actorgender from actor where year(actordob)=%s and actorgender=%s;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query2, (dob, gender))
        return cursor


def actors_dob(dob):
    # connect
    if (not conn):
        connect()

    query3 = "select actorname, monthname(actordob) as month, actorgender from actor where year(actordob)=%s;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query3, (dob))
        return cursor


def movie_studio():
    # connect
    if (not conn):
        connect()

    query4 = "select * from studio order by studioid asc;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query4)
        return cursor


def view_countries_table():
    # connect
    if (not conn):
        connect()

    query5 = "select * from country order by CountryID asc;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query5)
        return cursor


def add_country(cid, cname):
    # connect
    if (not conn):
        connect()

    ins = "INSERT INTO country (CountryID, CountryName) VALUES (%s, %s);"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(ins, (cid, cname))
        conn.commit()
        return cursor

def check_country(cid):
    # connect
    if (not conn):
        connect()

    query11 = "SELECT EXISTS(select countryid from country where CountryID = %s) as CheckExists"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query11, (cid))
        return cursor

def delete_country(cid):
    # connect
    if (not conn):
        connect()
    
    delete_c = "Delete from country where CountryID =%s;"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(delete_c, (cid))
        conn.commit()
        return cursor


def movie_sub(ids):
    # connect
    if (not conn):
        connect()

    query6 = "SELECT FilmName, SUBSTRING(FilmSynopsis, 1, 30) as FilmSynopsis FROM film WHERE FilmID IN (" + ids + ")"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query6)
        return cursor


def no_movieid(film_id):
    # connect
    if (not conn):
        connect()

    query9 = "SELECT EXISTS(select filmid from film where FilmID = %s) as CheckExists"

    with conn:
        conn.ping()
        cursor = conn.cursor()
        # execute the query made above
        cursor.execute(query9, (film_id))
        return cursor