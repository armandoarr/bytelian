import psycopg2
import sys
import pandas as pd


params = {
    "host": "localhost",
    "port": 5438,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
    }


def connect(params):
    conn = None

    try:
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as ex:
        print(ex)
        sys.exit(1)
    print("conexión a Postgres exitosa")
    return conn


def postgres_to_pd(conn, query, columns):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as ex:
        print("Hubo un error: %s" % ex)
        cursor.close()
        return 1

    resp = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(resp, columns=columns)
    return df
