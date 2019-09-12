from application import app, db
from flask import redirect, render_template, request, url_for
from application.forum.models import Topic
from application.forum.forms import TopicForm
from datetime import datetime

@app.route("/topics", methods=["GET"])
def topic_index():
    return render_template("topics/list.html", topics = Topic.query.all())

@app.route("/topics/new/")
def topic_form():
    return render_template("topics/new.html", form = TopicForm())

@app.route("/topics/<topic_id>/")
def edit_topic():
    return render_template("topics/edit.html", topic = Topic.query.get(topic_id), form = TopicForm())


@app.route("/topics/", methods=["POST"])
def topic_create():
    
    # title = Topic(request.form.get("title"))
    # bodytxt = Topic(request.form.get("bodytxt"))
    
    form = TopicForm(request.form)
    topic = Topic(form.title.data)
    topic.bodytxt = form.bodytxt.data
    # topic.date_created = datetime.now()

    db.session().add(topic)
    db.session().commit()

    return redirect(url_for("topic_index"))
