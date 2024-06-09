import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port = "5434")


cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS rates;')
cur.execute('CREATE TABLE rates (id serial PRIMARY KEY,'
                                 'to_currency varchar (150) NOT NULL,'
                                 'from_currency varchar (50) NOT NULL,'
                                 'rate NUMERIC(6,2) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

conn.commit()

cur.close()
conn.close()