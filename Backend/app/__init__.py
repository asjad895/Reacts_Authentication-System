from flask import Flask
from flask_cors import CORS
from .views import auth, profile, email, password_reset

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    app.config.from_object("config")

    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(email.bp)
    app.register_blueprint(password_reset.bp)

    return app
