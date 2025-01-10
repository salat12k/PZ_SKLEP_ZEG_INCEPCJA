import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Ścieżka do katalogu z plikiem __init__.py
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Konfiguracja bazy danych SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'watch_store.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Folder, w którym zapisywane będą przesłane pliki
    upload_folder = os.path.join(basedir, 'static', 'uploads')
    app.config["UPLOAD_FOLDER"] = upload_folder

    # (Opcjonalnie) Ograniczenie wielkości pliku do 16 MB
    # app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    db.init_app(app)

    # Import i rejestracja blueprintu
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Tworzymy tabele w bazie (jeśli jeszcze nie istnieją)
    with app.app_context():
        db.create_all()

    return app
