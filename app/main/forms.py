from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)], render_kw={'class': 'col-md-7'})
    body = TextAreaField('What is in your mind?', validators=[DataRequired()], render_kw={'class': 'col-md-14'})
    submit = SubmitField('Add Post')


class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
