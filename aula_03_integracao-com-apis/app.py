from flask import Flask, render_template
from controllers import routes

# Instancia Flask, informando o parâmetro "__main__" e a pasta views
app = Flask(__name__, template_folder='views')
routes.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    