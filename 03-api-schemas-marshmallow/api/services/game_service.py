from api import mongo
from ..models import game_model
from bson import ObjectId

class GameService:
    def add_game(game):
        result = mongo.db.games.insert_one({
            'title' : game.title,
            'descriptions': game.descriptions,
            'year' : game.year,
        })
        return mongo.db.games.find_one({'_id': ObjectId(result.inserted_id)})
    
    @staticmethod
    def get_games():
        return list(mongo.db.games.find())
    
    #para retornar apenas um jogo
    @staticmethod
    def get_game_by_id(id):
        return mongo.db.games.find_one({'_id': ObjectId(id)})
    
    #função para alterar um jogo
    def update_game(self, id):
        updated_game = mongo.db.games.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': {
                "title": self.title,
                "descriptions": self.descriptions,
                "year": self.year
            }}, 
            return_document=True
        )
        return updated_game
    
    @staticmethod
    def delete_game(id):
        mongo.db.games.delete_one({'_id': ObjectId(id)})