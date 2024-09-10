<<<<<<< HEAD
from flask import Flask
from controllers import routes

app = Flask(__name__, template_folder='views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
=======
from flask import Flask
from controllers import routes

app = Flask(__name__, template_folder='views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
>>>>>>> 224423c81ef74de5909895bd27128649fa1494e5
    