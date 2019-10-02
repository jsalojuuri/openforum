from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

# kirjautuminen
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Tarkista käyttäjänimi tai salasana ja lähetä tiedot uudelleen.")


    login_user(user)
    return redirect(url_for("forum_index")) 

# uloskirjautuminen
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

# rekisteröityminen
@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)
    # mahdolliset validoinnit

    username = User.query.filter_by(username=form.username.data).first()

    if username:
        return render_template("auth/registerform.html", form = form,
                               error = "Käyttäjätunnus jo käytössä. Valitse uusi käyttäjänimi ja lähetä tiedot uudelleen.")

    
    if not form.validate_on_submit():
        return render_template("auth/registerform.html", form = form,
                                error = "Nimen, käyttäjätunnuksen ja salasanan oltava 1-144 merkkiä pitkiä.")


    user = User(form.name.data, form.username.data, form.password.data)
    # user.username = form.username.data
    # user.password = form.password.data

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("auth_login")) 

