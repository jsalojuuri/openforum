from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")



class RegisterForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=1)])
    username = StringField("Käyttäjätunnus", [validators.Length(min=1)])
    password = PasswordField("Salasana", [validators.Length(min=1)])

    class Meta:
        csrf = False