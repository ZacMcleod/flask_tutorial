from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ


load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(255))
    model = db.Column(db.String(255))
    year = db.Column(db.Integer)

    def repr (self):
        return f'{self.year} {self.make} {self.model}'

# Schemas
class CarSchema (ma. Schema):
    class Meta:
        fields = ("id", "make", "model", "year")

car_schema = CarSchema()
cars_schema = CarSchema (many=True)

# Resources
class CarListResource(Resource):
    def get(self):
        all_cars = Car.query.all()
        return cars_schema.dump(all_cars)
    
    def post(self):
        print (request)
        new_car = Car(
            make=request.json ['make'], 
            model=request.json ['model'], 
            year=request.json ['year' ]
        )   
        db.session.add(new_car)
        db.session.commit()
        return car_schema.dump(new_car), 201

class CarResource(Resource):
    def get(self, car_id):
        car_from_db = Car.query.get_or_404(car_id)
        return car_schema.dump(car_from_db)
    def delete(self, car_id):
        car_from_db = Car.query.get_or_404(car_id)
        db.session.delete(car_from_db)
        return '', 204
# Routes
api.add_resource (CarListResource, '/api/cars')
api.add_resource(CarResource, '/api/cars/<int:car_id>')