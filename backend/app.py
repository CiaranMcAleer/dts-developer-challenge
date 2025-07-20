from flask import Flask, g
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'tasks.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        try:
            with open(schema_path, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")


import backend.routes


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run(debug=True, port=8080, host="0.0.0.0")
