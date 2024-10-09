from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/api)games'
api = Api(app)
mongo = PyMongo(app)
ma = Marshmallow(app)

from .resources import resources