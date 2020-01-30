from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError
from ..models import User, gender_enum, student_enum, staff_enum, parent_enum, religion_enum


class AddCourseForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64, "Please, Check Your Mail"), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log in")