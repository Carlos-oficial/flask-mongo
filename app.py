import os

from flask import Flask, render_template, session
import db 
from views.auth import auth
from flask_session import Session

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
    )
    app.config["MONGO_URI"] = "mongodb://localhost:27017"
    app.config["DB_NAME"] = "flask_db" 
    

    with app.app_context():
        db.init_db()
        db.init_app(app)

        app.config.from_mapping(
            SECRET_KEY="dev",
            SESSION_TYPE="mongodb",
            SESSION_MONGODB=db.get_instance(),
            SESSION_MONGODB_DB= app.config["DB_NAME"] ,
    )
    Session(app)


    app.register_blueprint(auth)

    @app.route("/",methods=["GET"])
    def index():
        return render_template("index.html",session=list(session.items()))

    @app.route("/routes")
    def routes():
        return [str(p) for p in app.url_map.iter_rules()]



    @app.route("/session")
    def session_data():
        return {str(p): session[p] for p in session}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
