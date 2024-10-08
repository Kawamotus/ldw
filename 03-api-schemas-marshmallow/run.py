from api import app, mongo
from api.models.game_model import Game
from api.services import game_service
from api.services.game_service import GameService

if __name__ == '__main__':
    with app.app_context():
        if 'games' not in mongo.db.list_collection_names():
            game = Game(
                title = '',
                descriptions= '',
                year = 0    
            )
            GameService.add_game(game)
    app.run(port=5000, debug=True)