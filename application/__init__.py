# Tuodaan Flask käyttöön
from flask import Flask
from functools import wraps
from flask_login import current_user

app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy

import os

# Heroku-ympäristössä käytössä Postgre
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

# Kehitysympäristössä käytössä SQLite 
else:
    # Käytetään forum.db-nimistä SQLite-tietokantaa. Kolme vinoviivaa
    # kertoo, että tiedosto sijaitsee tämän sovelluksen tiedostojen kanssa
    # samassa paikassa
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    # Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
    app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

# Kirjautuminen, osa 1
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

# roolit login_required annotaatiossa
def login_required(role="any"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "any":
                unauthorized = True

            if current_user.role == 'admin':
                unauthorized = False

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Oman sovelluksen toiminnallisuudet
from application import views

from application.forum import models
from application.forum import views

from application.auth import models
from application.auth import views

from application.admin import models
from application.admin import views

# kirjautuminen, osa 2
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass