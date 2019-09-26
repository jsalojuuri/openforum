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

# aiheen muokkaussivu
@app.route("/forum/<forum_id>/")
@login_required
def forum_topics(forum_id):

    if request.method == "GET":
        try:
            return render_template("topics/list.html", topics = Topic.query.filter_by(forum_id=forum_id).first())
        except Exception:
            return(str("Virhe"))
