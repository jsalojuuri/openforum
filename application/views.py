from application import app, db
from flask import redirect, render_template, request, url_for
from application.admin.models import Forum
from application.forum.models import Topic
from application.auth.models import User
from flask_login import current_user, login_required

# Open Forumin etusivu
@app.route("/")
def index():
    return render_template("index.html")

# Foorumeiden listaus (etusivu kirjautumisen jälkeen)
@app.route("/forums")
@login_required
def forum_index():
    return render_template("list.html", forums = Forum.forum_statistics_by_forum())