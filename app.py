from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decimal import Decimal
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv('.env')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Rates(db.Model):
    __tablename__ = "rates"
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.String())
    to_currency = db.Column(db.String()) 
    rate = db.Column(db.Numeric(6,2))
  

    def as_dict(self):
        return {r.name: getattr(self, r.name) 
        for r in self.__table__.columns}

    def __repr__(self):
        return '<Rate id={}>'.format(self.id)


@app.route('/convert', methods=['GET'])
def convert_currency():
 try:
  payload = request.get_json()
  amount = Decimal(payload['amount'])
  from_currency = payload['from_currency']
  to_currency = payload['to_currency']
 
  rate = Rates.query.filter_by(from_currency=from_currency,to_currency=to_currency).first()
  if rate is None:
   return jsonify({'error':'Conversion rate not found'}), 404

  conversion_rate = Decimal(rate.rate)
  converted_amount = amount * conversion_rate 

  response = {
    'amount': float(amount),
    'from_currency': from_currency,
    'to_currency': to_currency,
    'converted_amount': float(converted_amount)
  }
  return jsonify(response)
 except Exception as e:
  return jsonify({'error':str(e)}),500
 
@app.route('/rate', methods=['POST'])
def add_rate():
 try:
  payload = request.get_json()
  rate = payload['rate']
  from_currency = payload['from_currency']
  to_currency = payload['to_currency']

  rate = Rates.query.filter_by(from_currency=from_currency,to_currency=to_currency).first()
  if rate is not None:
   return jsonify({'error':'Conversion rate already exists'}), 400
  
  new_rate=Rates(from_currency=from_currency,to_currency=to_currency,rate=rate)
  db.session.add(new_rate)
  db.session.commit()
 
  response = {
    'rate': rate ,
    'from_currency': from_currency,
    'to_currency': to_currency,
  }
  
  return jsonify(response)
 except Exception as e:
  return jsonify({'error':str(e)}),500
 
@app.route('/rate', methods=['PUT'])
def update_rate():
 try:
  payload = request.get_json()
  rate = payload['rate']
  id = payload['id']
  
  existing_rate = Rates.query.filter_by(id=id).first()
  print(existing_rate)
  if existing_rate is None:
    return jsonify({'error':'rate with specified id does not exist' }), 404
  
  existing_rate.rate = rate
  db.session.commit()

  response = {
 "rate": rate,
 "id": id
}
  return jsonify (response)

 except Exception as e:
  return jsonify({'error':str(e)}),500
  
@app.route('/rate/<int:id>', methods=['GET'])
def get_rate_by_id(id):
 try:
  rate = Rates.query.filter_by(id=id).first()
  if  rate is None:
    return jsonify({'error':'rate not found' }), 404
  
  response = {
 "rate": rate.as_dict()
}
  return jsonify (response)

 except Exception as e:
  return jsonify({'error':str(e)}),500

@app.route("/rates",methods=['GET'])
def get_all_rates():
  try:
    rate_list = []
    rate = Rates.query.all()
    for element in rate:
     rate_list.append(element.as_dict())

    return jsonify({
      "rates": rate_list
    })
    
  except Exception as e:
   return jsonify({'error':str(e)}),500
  
@app.route("/rate/<int:id>", methods=['DELETE'])
def delete_rates(id):
    try:
        rate = Rates.query.get(id)

        if rate is not None:
            db.session.delete(rate)
            db.session.commit()
            return jsonify({'message': "Row deleted"})
        else:
            return jsonify({'message': "Row does not exist"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
if __name__ == '__main__':
  app.run(host="127.0.0.1",port=5000)
 