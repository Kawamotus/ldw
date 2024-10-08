from flask import Flask, render_template
from controllers import routes
from models.database import mongo, Game

app = Flask(__name__, template_folder='views')
routes.init_app(app)

#definindo string de conexao
app.config['MONGO_URI'] = 'mongo://localhost:27017/games'

if __name__ == '__main__':
    # Verifica no início da aplicação se o BD já existe. Caso contrário ele criará o BD.
    mongo.init_app(app=app)
    
    with app.app_context():
        if 'games' not in mongo.db.list_collection_names():
            game = Game(titulo='', ano=0, categoria='', plataforma='', quantidade=0, preco=0)
            game.save()
    app.run(host='localhost', port=5000, debug=True) 