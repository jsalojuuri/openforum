from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ForumForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=1, max=144)])
    description = StringField("Kuvaus")
 
    class Meta:
        csrf = False