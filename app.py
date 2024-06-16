from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

database_uri = os.getenv("DATABASE_URI")

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.String())
    to_currency = db.Column(db.String()) 
    rate = db.Column(db.Numeric(6,2))

    def __init__(self, to_currency, from_currency, rate):
        self.to_currency = to_currency
        self.from_currency = from_currency
        self.rate = rate

    def __repr__(self):
        return '<Result id={}>'.format(self.id)