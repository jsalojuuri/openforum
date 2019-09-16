from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TopicForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=1)])
    bodytxt = StringField("Text")
 
    class Meta:
        csrf = False