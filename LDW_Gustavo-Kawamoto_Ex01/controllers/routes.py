from flask import render_template, request
from datetime import date #usar pra inserir a data atual

def init_app(app):
    
    dt = f"{date.today().day}/{date.today().month}/{date.today().year}"
    itensHome = [{"Titulo": 1, "Autor": "Luan", "Data": dt, "Problema": "Defeito no computador"}, {"Titulo": 2, "Autor": "Vinicius", "Data": dt, "Problema": "Defeito na rede"}, {"Titulo": 3, "Autor": "Gustavo", "Data": dt, "Problema": "Celular não conecta"}, {"Titulo": 4, "Autor": "Alexandre", "Data": dt, "Problema": "Todos"}]
    solu = []
    
    @app.route("/", methods=["GET", "POST"])
    def home(): 
        
        if request.method == "POST":
            if request.form.get("autor") and request.form.get("descricao"):
                itensHome.append({"Titulo": len(itensHome) + 1, "Autor": request.form.get("autor"), "Problema": request.form.get("descricao"), "Data": dt})
        
        return render_template("index.html", itensHome=itensHome, dt=dt)
    
    @app.route("/solucoes", methods=["GET", "POST"])
    def solucoes():
        tSolu = len(solu)
        if request.method == "POST":
            if request.form.get("solucao"):
                solu.append(request.form.get("solucao"))
        
        return render_template("solucoes.html", dt=dt, solu=solu, tSolu=tSolu)
    
    @app.route("/resolvidos")
    def novos():
        return render_template("resolvidos.html", itensHome=itensHome)