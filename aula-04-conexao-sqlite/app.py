from flask import Flask, render_template
from controllers import routes
from models.database import db
import os

# Instancia Flask, informando o parâmetro "__main__" e a pasta views
app = Flask(__name__, template_folder='views')
routes.init_app(app)

#OS - Permite ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__)) 

#Passamos o diretório para o SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

if __name__ == "__main__":
    #passando a instancia do flask para a instancia do sqlalchmy
    db.init_app(app=app)
    #Criando um contexto de requisição ficticia
    with app.test_request_context():
        #Criando banco de dados caso não exista
        
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
    