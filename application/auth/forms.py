from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")



class RegisterForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=1)])
    lastname = StringField("Lastname")
    username = StringField("Käyttäjänimi", [validators.Length(min=1)])
    password = PasswordField("Salasana", [validators.Length(min=1)])

    class Meta:
        csrf = False