from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import Staff


class CourseForm(FlaskForm):
    teachers = Staff.query.filter_by(staff_class='TEACHER').all()

    course_name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    course_abr = StringField('Abbreviation', validators=[DataRequired(),   Length(1, 64)])
    course_max_score = StringField('Maximum Score', validators=[DataRequired()])
    course_success_score = StringField('Success Score', validators=[DataRequired()])
    course_teacher = SelectField('Select teacher', validators=[DataRequired()],
                                 choices=[(teacher.user.user_name, teacher.user.user_name) for teacher in teachers])


class AddCourseForm(CourseForm):
    submit = SubmitField("Add Course")


class EditCourseForm(CourseForm):
    submit = SubmitField("Edit Course")