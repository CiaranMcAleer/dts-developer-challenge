import sqlite3
from flask import g, current_app
import os

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        try:
            with open(schema_path, mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
