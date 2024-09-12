from flask import Flask
from controllers import routes
import os
from models.database import db

app = Flask(__name__, template_folder='views')
routes.init_app(app)

dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/ticketsDB.sqlite3')

app.config['SECRET_KEY'] = 'ticketzinhossecret'
app.config['PERMANENT_SESSIONLIFETIME'] = 3600

if __name__ == '__main__':
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(host="0.0.0.0", port=4000, debug=True)
    