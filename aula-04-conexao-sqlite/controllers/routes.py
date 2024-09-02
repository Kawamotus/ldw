import urllib.request
from flask import render_template, request, redirect, url_for
from datetime import date
import urllib
import json
from models.database import db, Game

jogadores = [] 
gamelist = [
    {"titulo": 'CS-GO', "ano": 2012, "categoria": "FPS Online"}
    ]

def init_app(app):    
    @app.route("/") # Decorador para o método app.route
    def home(): # View function
        data_atual = f'{date.today().day}/{date.today().month}/{date.today().year}'
        return render_template("index.html", data_atual=data_atual)

    @app.route("/games", methods=['GET', 'POST'])
    def games():
            
        titulo = "CS-GO"
        ano = 2012
        categoria = "FPS"
        anoAtual = date.today().year
        game = gamelist[0]
    
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))

                return redirect(url_for('games'))
        
        return render_template("games.html",
                               game=game, 
                               anoAtual=anoAtual,
                               jogadores=jogadores)
    
    @app.route("/cadgames", methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'titulo': request.form.get('titulo'), 'ano': request.form.get('ano'), 'categoria': request.form.get('categoria')})
                return redirect(url_for('cadgames'))
        return render_template("cadgames.html", gamelist=gamelist)
    
    @app.route("/apigames", methods=['GET', 'POST'])
    #criando rota com o parâmetro id
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url) 
        
        # Ler a resposta da requisicao (retorna JSON)
        data = res.read()
        # Converte o conteúdo da resposta JSON para dicionario Python
        gamesjson = json.loads(data)
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo=g
                    break
                
            if ginfo:
                return render_template("gameinfo.html", ginfo=ginfo)
            else:
                return f"Game com a id {id} não encontrado"

        else:
            return render_template("apigames.html", gamesjson=gamesjson)
        return render_template('apigames.html', gamesjson=gamesjson)
    
    #CRUD - Listagem
    @app.route("/estoque", methods=["GET", "POST"])
    @app.route("/estoque/delete/<int:id>", methods=["GET", "POST"])
    def estoque(id=None):
        #deletando um jogo
        if id:
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        #cadastrar um novo jogo
        if request.method == 'POST':
            newGame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            #Metodo SQLAlchemy para cadastrar no banco
            db.session.add(newGame)
            #Precisa commitar após inserir as info
            db.session.commit()
            return redirect(url_for('estoque'))
        else:
            #armazena em "gamesestoque" todos os valores, como um select e encaminha para a página
            gamesEstoque = Game.query.all()
            return render_template('estoque.html', gamesEstoque=gamesEstoque)
        
    @app.route('/edit/<int:id>', methods=["GET", "POST"])
    def edit(id):
        g = Game.query.get(id)
        #edita o jogo com as infos do form
        if request.method == "POST":
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            g.plataforma = request.form['plataforma']
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', g=g)    
        
    