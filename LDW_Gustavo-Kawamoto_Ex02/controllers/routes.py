from flask import render_template, request, redirect, url_for, flash, session
from datetime import date #usar pra inserir a data atual

from models.database import db, User, Ticket

def init_app(app):
    
    dt = f"{date.today().day}/{date.today().month}/{date.today().year}"
    
    @app.route("/", methods=["GET", "POST"])
    @app.route("/<int:ticketID>", methods=["GET", "POST"])
    def home(ticketID=None): 
        if ticketID:
            ticket = Ticket.query.get(ticketID)
            print(ticket)
            db.session.delete(ticket)
            db.session.commit()
            return redirect(url_for('home'))
        
        if request.method == "POST":
            ticketAuthor = request.form['ticketAuthor']
            ticketStatus = request.form['ticketStatus']
            ticketProblem = request.form['ticketProblem']
            ticketDate = dt
            
            print(request.form['ticketAuthor'])
            
            newTicket = Ticket(ticketAuthor=ticketAuthor, ticketDate=ticketDate, ticketProblem=ticketProblem, ticketStatus=ticketStatus)
            
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
        itensHome = Ticket.query.filter(Ticket.ticketStatus != '1').all()
        return render_template("resolvidos.html", itensHome=itensHome)
    
    @app.route("/editar/<int:ticketID>", methods=['GET', 'POST'])
    def editar(ticketID):
        ticket = Ticket.query.get(ticketID)
        
        if request.method == "POST":
            ticket.ticketAuthor = request.form['ticketAuthor']
            ticket.ticketStatus = request.form['ticketStatus']
            ticket.ticketProblem = request.form['ticketProblem']
            db.session.commit()
            return redirect(url_for('home'))
        
        return render_template('editar.html', ticket=ticket)