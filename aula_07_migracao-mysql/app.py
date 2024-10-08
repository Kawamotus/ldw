from flask import Flask, render_template
import pymysql.cursors
from controllers import routes
from models.database import db
import pymysql

# Instância do Flask, informando o parâmetro "__main__" e a pasta de views
app = Flask(__name__, template_folder='views')
routes.init_app(app)

#Define o nome do banco de dados
DB_NAME = 'games'
app.config['DATABASE_NAME'] = DB_NAME

#Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

# Secretkey
app.config['SECRET_KEY'] = 'thegamessecret'

# Define o tempo de duração da sessão (1 hora)
app.config['PERMANENT_SESSIONLIFETIME'] = 3600

# Define a pasta que receberá os arquivos de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Define o tamanho máximo de um arquivo de upload (16mb)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if __name__ == '__main__':
    #conectar ao mysql para criar o banco de dados
    connection = pymysql.connect(host='localhost', user='root', password='', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try: 
        with connection.cursor() as cursor:
            #cria o banco de dados se não existir
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print(f"O banco de dados {DB_NAME} foi criado")
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')
    finally:
        connection.close()
    
    #Inicializa a aplicação flask com o SQLAlchemy
    db.init_app(app=app)
    
    with app.app_context():
        #cria as tabelas
        db.create_all()
    #Inicia o servidor em localhost, porta 5000, modo de depuração ativo
    app.run(host='localhost', port=5000, debug=True)
