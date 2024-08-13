from flask import render_template, request
from datetime import date #usar pra inserir a data atual

def init_app(app):
    
    itensHome = [{"Titulo": "Ticket #1", "Autor": "Luan", "Data": date.today(), "Problema": "Defeito no computador"}, {"Titulo": "Ticket #2", "Autor": "Vinicius", "Data": date.today(), "Problema": "Defeito na rede"}, {"Titulo": "Ticket #3", "Autor": "Gustavo", "Data": date.today(), "Problema": "Celular não conecta"}, {"Titulo": "Ticket #4", "Autor": "Alexandre", "Data": date.today(), "Problema": "Todos"}]
    
    @app.route("/")
    def home():
        return render_template("index.html", itensHome=itensHome)
    
    @app.route("/cadastro")
    def cadastro():
        dt = date.today()
        return render_template("cadastro.html", dt=dt)