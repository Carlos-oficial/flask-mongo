from flask import g, current_app
from pymongo import MongoClient
import config

def get_instance():
    return MongoClient(current_app.config["MONGO_URI"])


def get_db():
    if "db" not in g:
        client = MongoClient(config.MONGO_URI)
        db = client.get_database(config.DB_NAME)
        g.db = db
        return db
    return g.db


def close_db():
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    g.db = get_db()


def init_app(app, teardown=False):
    if teardown:
        app.teardown_appcontext(close_db)


def get_data(data):
    if data is None:
        return None
    if data.get("_id"):
        data["_id"] = str(data["_id"])
    return data
