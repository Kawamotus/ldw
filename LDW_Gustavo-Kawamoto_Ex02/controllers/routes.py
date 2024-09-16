from flask import render_template, request, redirect, url_for, flash, session
from datetime import date #usar pra inserir a data atual
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

from models.database import db, User, Ticket

def init_app(app):
    
    dt = f"{date.today().day}/{date.today().month}/{date.today().year}"
    
    @app.before_request
    def checkout():
        routes = ['login', 'cadastro']
        if request.endpoint in routes:
            return
        
        if 'userID' not in session:
            return redirect(url_for('login'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            userLogin = request.form['userLogin']
            userPassword = request.form['userPassword']
            print(userLogin, userPassword)
            user = User.query.filter_by(userLogin=userLogin).first()
            
            if user and check_password_hash(user.userPassword, userPassword):
                session['userID'] = user.userID
                session['userName'] = user.userName
                session['userLogin'] = user.userLogin
                session['userEmail'] = user.userEmail
                
                flash(f"Login bem sucedido, bem vindo(a) {session['userName']}", 'success')
                
                return redirect(url_for('home'))
            
            
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
    
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            userName = request.form['userName']
            userLogin = request.form['userLogin']
            userEmail = request.form['userEmail']
            userPassword = request.form['userPassword']
            
            userLoginVerify = User.query.filter_by(userLogin=userLogin).first()
            userEmailVerify = User.query.filter_by(userEmail=userEmail).first()
            
            if userLoginVerify or userEmailVerify:
                msg = Markup("Usuário já cadastrado, faça o <a href='/login'>Login</a>")
                flash(msg, "danger")
                return redirect(url_for('cadastro'))
            else:
                hashPassword = generate_password_hash(userPassword, method='scrypt')
                newUser = User(userName=userName, userLogin=userLogin, userEmail=userEmail, userPassword=hashPassword)
                db.session.add(newUser)
                db.session.commit()
                flash('Cadastrado com sucesso, faça o login!', "success")
                return redirect(url_for('login'))
                
        return render_template('cadastro.html')
    
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
