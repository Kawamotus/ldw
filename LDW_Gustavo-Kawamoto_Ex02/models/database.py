from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(150))
    userLogin = db.Column(db.String(150))
    userEmail = db.Column(db.String(150))
    userPassword = db.Column(db.String(120))
    
    def __init__(self, userName, userEmail, userPassword, userLogin):
        self.userName = userName
        self.userLogin = userLogin
        self.userEmail = userEmail
        self.userPassword = userPassword
    

class Ticket(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    ticketAuthor = db.Column(db.String(150))
    ticketDate = db.Column(db.String(11))
    ticketProblem = db.Column(db.String(256))
    ticketStatus = db.Column(db.String(1))
    
    def __init__(self, ticketAuthor, ticketDate, ticketProblem, ticketStatus):
        self.autor = ticketAuthor
        self.data = ticketDate
        self.problema = ticketProblem
        self.ticketStatus = ticketStatus
        