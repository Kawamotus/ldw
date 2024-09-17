import urllib.request
from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import Markup
from datetime import date
import urllib # Lê a URL da API
import json # JSON conversão do formato
import os
import uuid
from models.database import db, Game, User, Imagem
from werkzeug.security import generate_password_hash, check_password_hash


jogadores = []
gamelist = [{'Título': 'CS-GO',
        'Ano': 2012,
        'Categoria': 'FPS Online'}]


def init_app(app):
    #função de middleware para verificar a autenticação do user
    @app.before_request
    def checkout():
        #rotas que não precisam de login
        routes = ['login', 'caduser', 'home']
        
        #se a rota não requerir auth, ele permite o acesso
        if request.endpoint in routes or request.path.startswith('/static'):
            return
        
        #se o user não estiver autenticado redireciona para o login
        if 'userId' not in session:
            return redirect(url_for('login'))
    
    @app.route("/")  # Decorator para o método app.route
    def home():  # View function (função de visão)
        dataAtual = f'{date.today().day}/{date.today().month}/{date.today().year}.'
        # Renderizando a página HTML
        return render_template('index.html', dataAtual=dataAtual)
        # return '<h1>Iniciando com o Flask...</h1>'

    @app.route("/games", methods=['GET', 'POST'])
    def games():
        # titulo = "CS-GO"
        # ano = 2012
        # categoria = "FPS"
        anoAtual = date.today().year  # .day .month
        game = gamelist[0]
        
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
            return redirect(url_for('games'))

        return render_template('games.html',
                               game=game,
                               anoAtual=anoAtual,
                               jogadores=jogadores)

    @app.route("/cadgames", methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'Título' : request.form.get('titulo'), 
                                 'Ano' : request.form.get('ano'), 
                                 'Categoria' : request.form.get('categoria')})
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html', gamelist=gamelist)
    
    @app.route('/apigames', methods=['GET', 'POST'])
    # Criando a rota com o parâmetro ID
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        # URL da API
        # url = 'http://10.67.57.11:5000'
        url = 'https://www.freetogame.com/api/games'
        # Fazendo a requisição GET para a URL (retorna um objeto)
        res = urllib.request.urlopen(url)
        # Ler a reposta da requisição (retorna um JSON)
        data = res.read()
        # Converte o conteúdo da resposta JSON para dicionário Python
        gamesjson = json.loads(data)
        # Verificando se o ID do jogo foi passado
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo=g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:            
            return render_template('apigames.html', gamesjson=gamesjson)
        
    # CRUD - Listagem  
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>', methods=['GET', 'POST'])
    def estoque(id=None):
        # Deletando um jogo
        if id:
            # Selecionando o jogo
            game = Game.query.get(id)
            # Deletar pela ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))            
        # Cadastrar um novo jogo
        if request.method == 'POST':
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            # Método do SQLAlchemy para cadastrar no banco
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        else:
            # PAGINAÇÃO
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo de dado inteiro
            page = request.args.get('page', 1, type=int)
            # Define o número de registros por página
            per_page = 3
            # Armazena em "gamesestoque" todos os valores, como um SELECT e encaminha para página
            # gamesestoque = Game.query.all()
            # Filtrando os registros de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)
    
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        game = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            game.titulo = request.form['titulo']
            game.ano = request.form['ano']
            game.categoria = request.form['categoria']
            game.plataforma = request.form['plataforma']
            game.preco = request.form['preco']
            game.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)
    
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['email']
            password = request.form['password']
            #print(username, password)
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                #print("Logado com sucesso")
                session['userId'] = user.id
                session['username'] = user.username
                #gambiarra pq nao cadastramos no banco
                nickname = user.username.split("@")
                flash(f"Login bem sucedido! Bem vindo {nickname[0]}", 'success')        
                return redirect(url_for('home'))
            else:
                flash("Falha no Login! Verifique seu usuário e senha!", 'danger')  
        return render_template('login.html')
    
    @app.route("/caduser", methods=['GET', 'POST'])
    def caduser():
       
        
        if request.method == 'POST':
            #fomos cabaços, cadastramos email no codigo e é username
            username = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                msg = Markup("Usuário já cadastrado. Faça <a href='/login'>login</a>")
                flash(msg, 'danger')
                return redirect(url_for('caduser'))
            else:
                hashedPassword = generate_password_hash(password, method='scrypt')
                newUser = User(username=username, password=hashedPassword)
                db.session.add(newUser)
                db.session.commit()
                flash("REgistro realizado com sucesso, faça o login!", 'success')
                return redirect(url_for('login'))
        return render_template('caduser.html')
    
    @app.route('/logout', methods=["GET", "POST"])
    def logout():
        session.clear()
        return redirect(url_for('home'))
    
    #definindo os tipos de arquivos permitidos
    #set cria conjunto, que é mais eficiente para esse caso
    FILE_TYPES = set(['png', 'jpeg', 'jpg', 'gif', 'webp', 'jfif'])
    #retorna se a extensão do arquivo está na lista
    def arquivosPermitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
    
    @app.route('/galeria', methods=['GET', 'POST'])
    @app.route('/galeria/delete/<int:id>', methods=['GET', 'POST'])
    def galeria(id=None):
        imagens = Imagem.query.all()
        
        if id:
            image = Imagem.query.get(id)
            db.session.delete(image)
            db.session.commit()
            return redirect(url_for('galeria')) 
        
        if request.method == "POST":
            #caoturando o arquivos que retornou do formulário
            file = request.files['file']
            
            #verifica se a ext do arquivo é permitida
            if not arquivosPermitidos(file.filename):
                flash('Utilize somente os tipos de arquivos de imagens', 'danger')
                return redirect(request.url)
            #define um nome aleatório para o arquiv
            filename = str(uuid.uuid4())
            ext = file.filename.rsplit('.', 1)[1].lower()
            fname = f'{filename}.{ext}'
            
            #salva no banco
            img = Imagem(fname)
            db.session.add(img)
            db.session.commit()
            #salva o arquivo na pasta uploads
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
            flash('Imagem enviada com sucesso', 'success')
            return redirect(url_for('galeria'))
        return render_template('galeria.html', imagens=imagens)