from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TopicForm(FlaskForm):
    title = StringField("Otsikko", [validators.Length(min=1)])
    bodytxt = StringField("Teksti")
 
    class Meta:
        csrf = False