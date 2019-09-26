from application import app, db
from flask import redirect, render_template, request, url_for
from application.forum.models import Topic, Topicaccount
from application.forum.forms import TopicForm
from application.auth.models import User
from application.auth.forms import RegisterForm
from application.admin.models import Forum
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required

# kirjoitusten (aiheiden) listaus
@app.route("/forum/<forum_id>/topics", methods=["GET"])
@login_required
def topic_index(forum_id):
    
    return render_template("topics/list.html", forums = Forum.query.filter_by(id=forum_id), topics = Topic.find_topics_by_forum(forum_id), form = TopicForm())

# lisää kirjoitus -lomake
@app.route("/forum/<forum_id>/topics/create", methods=["POST"])
@login_required
def topic_create(forum_id):
    
    form = TopicForm(request.form)
    
    if not form.validate_on_submit():
        return render_template('topics/list.html', forums = Forum.query.filter_by(id=forum_id), topics = Topic.find_topics_by_forum(forum_id), form=form,
                                error = "Otsikon tulee olla vähintään 1 merkkiä pitkä")

    topic = Topic(form.title.data, form.bodytxt.data)
    topic.forum_id = forum_id
    db.session().add(topic)
    db.session.flush()

    topicAccount = Topicaccount(True, False)
    topicAccount.account_id = current_user.id
    topicAccount.topic_id = topic.id
    db.session.add(topicAccount)
    
    db.session().commit()

    return redirect(url_for("topic_index", forum_id = forum_id))

# poista nappi (kirjoituksen poistava lomake)
@app.route("/forum/<forum_id>/topics/delete", methods=["POST"])
@login_required
def topic_delete(forum_id):
    
    topic_id = request.form.get("topic_id")
    topic = Topic.query.filter_by(id=topic_id).first()
    db.session.delete(topic)
    db.session.commit()
    
    return redirect(url_for("topic_index", forum_id=forum_id))

# kirjoituksen (aiheen) muokkaussivu
@app.route("/forum/<forum_id>/topic/<topic_id>/")
@login_required
def topic_update(forum_id, topic_id):

    topic=Topic.query.filter_by(id=topic_id).first()
    topic_id=topic.id
    title=topic.title

    if request.method == "GET":
        try:
            return render_template("topics/topic.html", topics=Topic.query.filter_by(id=topic_id), forum_id=forum_id, topic_id=topic_id, form=TopicForm(title=title))
        except Exception:
            return(str("Virhe"))

# Muokatun kirjoituksen (aiheen) lähetyslomake
@app.route("/forum/<forum_id>/topic/update", methods=["POST"])
@login_required
def topic_update_post(forum_id):
    
    form=TopicForm(request.form)
    topic_id = request.form.get("topicid")

    if not form.validate_on_submit():
        title=Topic.query.filter_by(id=topic_id).first().title
        return render_template("topics/topic.html", topics=Topic.query.filter_by(id=topic_id), forum_id=forum_id, topic_id=topic_id, form=TopicForm(title=title),
                                error = "Otsikon tulee olla vähintään 1 merkkiä pitkä")

    topic = Topic.query.filter_by(id=topic_id).first()
    topic.title = form.title.data
    topic.bodytxt = request.form.get("newbodytxt")
    db.session.commit()
    
    return redirect(url_for("topic_index", forum_id=forum_id))

# käyttäjän profiilisivu
@app.route("/user/ownpage", methods=["GET", "POST"])
@login_required
def user_ownpage():

    user = current_user

    return render_template("user/profile.html", user = user, topics = Topic.find_user_topics(current_user.id), 
                    stats = Topic.find_user_statistics(current_user.id), form=RegisterForm(name=user.name, username=user.username, password=user.password))

# Käyttäjätietojen muokkauslomake
@app.route("/user/profile/", methods=["POST"])
@login_required
def user_profile_update():

    
    form = RegisterForm(request.form)
    user = current_user
    username = User.query.filter_by(username=form.username.data).first()

    if username and user != username:
        return render_template("user/profile.html", user = user, topics = Topic.find_user_topics(current_user.id), 
                    stats = Topic.find_user_statistics(current_user.id), form=RegisterForm(name=user.name, username=user.username, password=user.password),
                               error = "Käyttäjätunnus jo käytössä. Valitse uusi käyttäjänimi ja lähetä tiedot uudelleen.")

    if not form.validate_on_submit():
        return render_template("user/profile.html", user = user, topics = Topic.find_user_topics(current_user.id), 
                    stats = Topic.find_user_statistics(current_user.id), form=RegisterForm(name=user.name, username=user.username, password=user.password),
                    error = "Nimen, käyttäjätunnuksen ja salasanan oltava vähintään 1 merkkiä pitkiä.")

    user = User.query.filter_by(id=user.id).first()
    user.name = form.name.data
    user.username = form.username.data
    user.password = form.password.data
    db.session.commit()
    
    return redirect(url_for("user_ownpage"))

