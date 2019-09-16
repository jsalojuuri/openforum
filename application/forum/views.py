from application import app, db
from flask import redirect, render_template, request, url_for
from application.forum.models import Topic
from application.forum.forms import TopicForm
from application.auth.models import User
from application.auth.forms import RegisterForm
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required

# aiheiden listaus
@app.route("/topics", methods=["GET"])
@login_required
def topic_index():
    return render_template("topics/list.html", topics = Topic.query.all())

# aiheen poistaminen
@app.route("/topics/delete", methods=["POST"])
@login_required
def topic_delete():
    title = request.form.get("title")
    topic = Topic.query.filter_by(title=title).first()
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for("topic_index"))

# uuden aiheen lomakesivu
@app.route("/topics/new/")
@login_required
def topic_form():
    return render_template("topics/new.html", form = TopicForm())

# aiheen muokkaussivu
@app.route("/topics/<topic_id>/")
@login_required
def topic_update(topic_id):

    if request.method == "GET":
        try:
            return render_template("topics/topic.html", topics=Topic.query.filter_by(id=topic_id))
        except Exception:
            return(str("Virhe"))

# Muokatun aiheen lähetys
@app.route("/topics/update/", methods=["POST"])
@login_required
def topic_update_post():
    
    topicid = request.form.get("topicid")
    newtitle = request.form.get("newtitle")
    newbodytxt = request.form.get("newbodytxt")
 
    topic = Topic.query.filter_by(id=topicid).first()
    topic.title = newtitle
    topic.bodytxt = newbodytxt
    db.session.commit()
    
    return redirect(url_for("topic_index"))

# uuden aiheen lähettäminen
@app.route("/topics/", methods=["POST"])
@login_required
def topic_create():
    
    form = TopicForm(request.form)
    
    if not form.validate_on_submit():
        return render_template('topics/new.html', form=form,
                                error = "Otsikon tulee olla vähintään 1 merkkiä pitkä")

    topic = Topic(form.title.data, form.bodytxt.data)
    topic.account_id = current_user.id

    db.session().add(topic)
    db.session().commit()

    return redirect(url_for("topic_index"))

# käyttäjän profiilisivu
@app.route("/user/ownpage", methods=["GET", "POST"])
@login_required
def user_ownpage():
    return render_template("user/profile.html", user = current_user)

# Käyttäjätietojen muokkaus
@app.route("/user/profile/", methods=["POST"])
@login_required
def user_profile_update():

    username = request.form.get("username")
    newname = request.form.get("newname")
    newusername = request.form.get("newusername")
    newpassword =request.form.get("newpassword")
    user = User.query.filter_by(username=username).first()
    user.name = newname
    user.username = newusername
    user.password = newpassword
    db.session.commit()
    
    return redirect(url_for("user_ownpage"))

