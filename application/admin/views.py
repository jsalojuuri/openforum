from application import app, db, login_required
from flask import redirect, render_template, request, url_for
from application.admin.models import Forum
from application.admin.forms import ForumForm
from application.forum.models import Topic
from flask_login import current_user

# admin-paneelin etusivu
@app.route("/admin", methods=["GET", "POST"])
@login_required(role="admin")
def admin_panel():
    return render_template("admin/panel.html", forums = Forum.forum_statistics_by_forum(), form = ForumForm(), stats = Forum.forum_statistics())

# uuden foorumin lisääminen lomakkeella
@app.route("/admin/forums/add", methods=["POST"])
@login_required(role="admin")
def forum_create():
    
    form = ForumForm(request.form)
    forum_name = Forum.query.filter_by(name=form.name.data).first()

    # tarkista onko saman niminen foorumi jo olemassa
    if forum_name:
        return render_template("admin/panel.html", forums = Forum.forum_statistics_by_forum(), form=form, stats = Forum.forum_statistics(),
                               error = "Saman niminen foorumi on jo luotu. Muuta foorumin nimeä ja lähetä lomake uudelleen")

    # lomakkeen validointi
    if not form.validate_on_submit():
        return render_template('admin/panel.html', forums = Forum.forum_statistics_by_forum(), form=form, stats = Forum.forum_statistics(),
                                error = "Foorumin nimen on oltava 1-144 merkkiä pitkä")

    forum = Forum(form.name.data)
    forum.description = form.description.data
    db.session().add(forum)
    db.session().commit()

    return redirect(url_for("admin_panel"))

# foorumeiden muokkaus lomakkeella
@app.route("/admin/forums/update", methods=["POST"])
@login_required(role="admin")
def forum_update_form():

    form = ForumForm(request.form)
    name = form.name.data
    description = request.form.get("newdescription")
    forum_id = request.form.get("forumid")
    forum = Forum.query.filter_by(id=forum_id).first()
    
    # lomakkeen validointi
    if not form.validate_on_submit():
            return render_template("admin/update_forum.html", forum=forum, form=ForumForm(name=name, description=description),
                                        error = "Foorumin nimen on oltava 1-144 merkkiä pitkä")

    forum.name = name    
    forum.description = description
    db.session.commit()
    
    return redirect(url_for("admin_panel"))

# foorumin muokkaussivu
@app.route("/admin/forums/<forum_id>/")
@login_required(role='admin')
def forum_update(forum_id):

    forum = Forum.query.filter_by(id=forum_id).first()
    name = forum.name
    description = forum.description

    if request.method == "GET":
        try:
            return render_template("admin/update_forum.html", forum=forum, form=ForumForm(name=name, description=description))
        except Exception:
            return(str("Virhe"))

# foorumin poistaminen napilla
@app.route("/admin/forums/delete", methods=["POST"])
@login_required(role='admin')
def forum_delete():
    name = request.form.get("name")
    forum = Forum.query.filter_by(name=name).first()
    topics = Topic.query.filter_by(forum_id=forum.id)
    
    for topic in topics:
        db.session.delete(topic)
    
    db.session.delete(forum)
    db.session.commit()
    return redirect(url_for("admin_panel"))