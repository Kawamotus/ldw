from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# Instância do Flask, informando o parâmetro "__main__" e a pasta de views
app = Flask(__name__, template_folder='views')
routes.init_app(app)

# OS - Permite ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

# Passamos o diretório para o SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(dir, 'models/games.sqlite3')
    
#Secret key (precisa pra funcionar o lixo da sessão)
app.config['SECRET_KEY'] = 'thegamessecret'
#Define o tempo de duração da sessão
app.config['PERMANENT_SESSIONLIFETIME'] = 3600

if __name__ == '__main__':
    # Passando a instância do Flask para a instância do SQLAlchemy
    db.init_app(app=app)
    # Criando um contexto de requisição fictícia
    with app.test_request_context():
        # Criando o banco caso não exista
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
