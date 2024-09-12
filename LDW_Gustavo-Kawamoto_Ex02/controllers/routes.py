from flask import render_template, request, redirect, url_for, flash, session
from datetime import date #usar pra inserir a data atual

from models.database import db, User, Ticket

def init_app(app):
    
    dt = f"{date.today().day}/{date.today().month}/{date.today().year}"
    
    @app.route("/", methods=["GET", "POST"])
    def home(id=None): 
        
        if request.method == "POST":
            ticketAuthor = request.form['ticketAuthor']
            ticketStatus = request.form['ticketStatus']
            ticketProblem = request.form['ticketProblem']
            ticketDate = dt
            
            newTicket = Ticket(ticketAuthor=ticketAuthor, ticketStatus=ticketStatus, ticketProblem=ticketProblem, ticketDate=ticketDate)
            
            db.session.add(newTicket)
            db.session.commit()
            
            return redirect(url_for('home'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page=5
            
            itensHome = Ticket.query.paginate(page=page, per_page=per_page)
            return render_template("index.html", itensHome=itensHome)
    
    @app.route("/resolvidos")
    def novos():
        itensHome = "a"
        return render_template("resolvidos.html", itensHome=itensHome)