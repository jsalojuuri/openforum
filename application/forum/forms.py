from flask_wtf import FlaskForm
from wtforms import StringField, validators

class TopicForm(FlaskForm):
    title = StringField("Otsikko", [validators.Length(min=1, max=144)])
    bodytxt = StringField("Teksti")
 
    class Meta:
        csrf = False


class CommentForm(FlaskForm):
    bodytxt = StringField("Teksti", [validators.Length(min=1, max=1444)])
 
    class Meta:
        csrf = False