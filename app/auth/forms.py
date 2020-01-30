from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError
from ..models import User, gender_enum, student_enum, staff_enum, parent_enum, religion_enum

STAFF_OFFSET = 2


def enum_to_list_of_tuples(enum):
    return [(en.value, en.name.capitalize()) for en in enum]


def add_offset_to_tuples(list_of_tuples, offset):
    return [(tp[0] + offset, tp[1]) for tp in list_of_tuples]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64, "Please, Check Your Mail"), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log in")


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64, "Please, Check Your Mail Length. Max(64 char)"), Email()])
    user_name = StringField('User Name', validators=[DataRequired(), Length(1, 64),
                                                     Regexp('^[A-Za-z]*[.][A-Za-z]*[0-9]*$', 0,
                                                            'Username must have be in this format:'
                                                            ', (letters.letters)(numbers) like Ahmed.Mohamed123')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm',
                                                                             message='Password must match.')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    user_type = SelectField('Select registration type', validators=[DataRequired()], coerce=int,
                            choices=[(1, 'Student'), (2, 'Parent')] + add_offset_to_tuples(
                                enum_to_list_of_tuples(staff_enum), STAFF_OFFSET))
    submit = SubmitField("Next")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_user_name(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('Username is already in use.')


class UserMainFieldForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name', validators=[DataRequired(), Length(1, 32)])
    middle_name = StringField('Middle Name', validators=[DataRequired(), Length(1, 32)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(1, 32)])
    mobile_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    gender = SelectField('Select Gender', validators=[DataRequired()], coerce=int,
                         choices=enum_to_list_of_tuples(gender_enum))
    religion = SelectField('Select Religion', validators=[DataRequired()], coerce=int,
                           choices=enum_to_list_of_tuples(religion_enum))
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')


class StudentForm(UserMainFieldForm):
    student_class = SelectField('Select Class', validators=[DataRequired()], coerce=int,
                                choices=enum_to_list_of_tuples(student_enum))
    submit = SubmitField("Register")


class ParentForm(UserMainFieldForm):
    parent_class = SelectField('Select Parent', validators=[DataRequired()], coerce=int,
                               choices=enum_to_list_of_tuples(parent_enum))
    student_username = StringField('Enter your Student Username', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField("Register")

    def validate_student_username(self, field):
        if not User.query.filter_by(user_name=field.data).first():
            raise ValidationError('Student username is not already registered.')


class StaffForm(UserMainFieldForm):
    submit = SubmitField("Register")


