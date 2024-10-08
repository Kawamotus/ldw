from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class Game():    
    def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.plataforma = plataforma
        self.preco = preco
        self.quantidade = quantidade
        
    def save(self):
        mongo.db.games.insert_one({
            'título': self.titulo,
            'ano': self.ano,
            'categoria': self.categoria,
            'plataforma': self.plataforma,
            'preco': self.preco,
            'quantidade': self.quantidade
        })
    
    #metodo para listar
    @staticmethod
    def get_all():
        return list(mongo.db.games.find())