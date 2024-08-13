from flask import render_template, request
from datetime import date

def init_app(app):
    lista = []
    gameList = [{"Titulo": "CS-GO", "Ano": 2012, "Categoria": "FPS"}]
    
    @app.route("/") #Decorator com o método app.route
    def home(): #view function
        dataAtual = date.today()
        return render_template('index.html', dataAtual=dataAtual) #Renderizando a página html
        
    @app.route("/games", methods=["GET", "POST"])
    def games():
        # titulo = "CS-GO"
        # ano = 2012
        # categoria = "FPS"
        anoAtual = date.today().year #pode ser day, month
        
        if request.method == "POST":
            #entre parenteses no get coloca o nome do form
            if request.form.get("jogador"):
                lista.append(request.form.get('jogador'))
        
        game = gameList[0]
        return render_template('games.html', game = game, anoAtual=anoAtual, lista=lista)        
    
    @app.route("/cadgames", methods=["GET", "POST"])
    def cadgames():
        
        if request.method == "POST":
            if request.form.get("titulo") and request.form.get("ano") and request.form.get("categoria"):
                gameList.append({"Titulo": request.form.get("titulo"), "Ano": request.form.get("ano"), "Categoria": request.form.get("categoria") } )
        return render_template("cadgames.html", gameList=gameList)