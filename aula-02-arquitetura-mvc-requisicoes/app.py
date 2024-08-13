from flask import Flask, render_template
from controllers import routes

#instância do flask, informando o parâmetro __main__ (o arquivo que está sendo executado se torna a main) e a pasta views
app = Flask(__name__, template_folder='views')

routes.init_app(app)
        
        
if __name__ == '__main__':
    #port é opcional, o padrão é 5000
    #debug é pra atualizar sozinho e indicar erros
    #host é onde ta rodando o role, por padrão localhost
    app.run(host="localhost", port=4000, debug=True)