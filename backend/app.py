from flask import Flask
from flask_cors import CORS
import os
from .db import get_db, close_connection, init_db

app = Flask(__name__)
CORS(app)
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'tasks.db')
app.teardown_appcontext(close_connection)
# Register Blueprint after app is created


from .routes import routes as routes_blueprint
app.register_blueprint(routes_blueprint)


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run()
