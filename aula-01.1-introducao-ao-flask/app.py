from flask import Flask, render_template
from datetime import date

#instância do flask, informando o parâmetro __main__ (o arquivo que está sendo executado se torna a main) e a pasta views
app = Flask(__name__, template_folder='views')

@app.route("/") #Decorator com o método app.route
def home(): #view function
    dataAtual = date.today()
    return render_template('index.html', dataAtual=dataAtual) #Renderizando a página html
        
@app.route("/games")
def games():
    # titulo = "CS-GO"
    # ano = 2012
    # categoria = "FPS"
    anoAtual = date.today().year #pode ser day, month
    lista = ["Gustavo", "Vinicius", "Vinicius", "Renato"]
    game = {"Titulo": "CS-GO", "Ano": 2012, "Categoria": "FPS"}
    return render_template('games.html', game = game, anoAtual=anoAtual, lista=lista)        
        
        
if __name__ == '__main__':
    #port é opcional, o padrão é 5000
    #debug é pra atualizar sozinho e indicar erros
    #host é onde ta rodando o role, por padrão localhost
    app.run(host="localhost", port=4000, debug=True)