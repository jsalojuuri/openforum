from flask_wtf import FlaskForm
from wtforms import StringField

class TopicForm(FlaskForm):
    title = StringField("Title")
    bodytxt = StringField("Text")
 
    class Meta:
        csrf = False