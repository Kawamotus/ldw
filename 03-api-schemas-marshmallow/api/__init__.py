from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

# Criando a instância do Flask
app = Flask(__name__)

# String de conexão MongoDB
app.config["MONGO_URI"] = 'mongodb://localhost:27017/api_games'

# Criando a instância de Api do flask_restful e passando o Flask
api = Api(app)

# Instância do PyMongo
mongo = PyMongo(app)

# Instância do Marshmallow
ma = Marshmallow(app)

from .resources import game_resource