import psycopg2
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy(app)

conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="12345",
        port = "5432")


cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS rates;')
cur.execute('CREATE TABLE rates (id serial PRIMARY KEY,'
                                 'to_currency varchar (150) NOT NULL,'
                                 'from_currency varchar (50) NOT NULL,'
                                 'rate NUMERIC(6,2) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )



class Result(db.Model):
 def __init__(self,id,to_currency,from_currency,rates):
     id = db.Column(db.Integer, primary_key=True)
     from_currency = db.Column(db.String())
     to_currency = db.Column(JSON)
     rates = db.Column(JSON)

def __init__(self,to_currency,from_currency,rate):
     self.to_currency = to_currency
     self.from_currency = from_currency
     self.rate = rate

def __repr__(self):
 return '<id {}>'.format(self.id)

conn.commit()

cur.close()
conn.close()