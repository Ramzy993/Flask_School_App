from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from enum import IntEnum
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class gender_enum(IntEnum):
    Male = 1
    FEMALE = 2


class religion_enum(IntEnum):
    MUSLIM = 1
    CRISTIAN = 2
    JEWISH = 3


class student_enum(IntEnum):
    GRADE10 = 1
    GRADE11 = 2
    GRADE12 = 3


class staff_enum(IntEnum):
    TEACHER = 1
    MANAGEMENT = 2
    ADMIN = 3


class parent_enum(IntEnum):
    FAHTER = 1
    MOTHER = 2
    SISTER = 3
    BROTHER = 4


class Permission:
    VIEW_RESULTS = 1
    EDIT_RESULTS = 2
    VIEW_COURSES = 4
    EDIT_COURSES = 8
    VIEW_NEWS_FEED = 16
    VIEW_DASHBOARD = 32
    ADMIN = 64

    roles = {
        'Student': [VIEW_RESULTS, VIEW_COURSES, VIEW_NEWS_FEED],
        'Parent': [VIEW_RESULTS],
        'Teacher': [VIEW_RESULTS, EDIT_RESULTS, EDIT_COURSES, VIEW_COURSES, VIEW_NEWS_FEED],
        'Management': [VIEW_RESULTS, VIEW_COURSES, VIEW_DASHBOARD],
        'Administrator': [VIEW_RESULTS, EDIT_RESULTS, EDIT_COURSES, VIEW_COURSES, VIEW_NEWS_FEED, VIEW_DASHBOARD, ADMIN]
    }


class User(db.Model, UserMixin):
    __tabelname__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hashed = db.Column(db.String(128))
    is_confirmed = db.Column(db.Boolean, default=False)

    user_role = db.relationship('UserRole', backref='user', uselist=False)
    user_contacts = db.relationship('UserContact', backref='user', uselist=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    student = db.relationship('Student', backref='user', uselist=False)
    parent = db.relationship('Parent', backref='user', uselist=False)
    staff = db.relationship('Staff', backref='user', uselist=False)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password_hashed = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
        return check_password_hash(self.password_hashed, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.is_confirmed = True
        db.session.add(self)

        return True

    def can(self, perm):
        return self.user_role is not None and self.user_role.has_permission(perm)

    def is_administrator(self):
        return self.can(sum(Permission.roles['Administrator']))

    def generate_auth_tokken(self, expiration=3600):
        s = Serializer(current_app.congig['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, }).decode('utf-8')


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class UserRole(db.Model):
    __tabelname__ = 'users_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(UserRole, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    def add_permissions(self, perms):
        for perm in perms:
            if not self.has_permission(perm):
                self.permission += perm

    def remove_permissions(self, perms):
        for perm in perms:
            if not self.has_permission(perm):
                self.permission -= perm

    def reset_permission(self):
        self.permission = 0

    def has_permission(self, perm):
        return self.permission & perm == perm

    def return_role(self):
        keys_list = Permission.roles.keys()
        values_list = [sum(value) for value in Permission.roles.values()]
        return list(keys_list)[values_list.index(self.permission)]


class UserContact(db.Model):
    __tabelname__ = 'users_contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    mobile_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(64), nullable=False)

    def __init__(self, mobile_number, address):
        self.mobile_number = mobile_number
        self.address = address


class Post(db.Model):
    __tabelname__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def return_user_name(self):
        return User.query.filter_by(id=self.author_id).first().user_name


class Comment(db.Model):
    __tabelname__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, body):
        self.body = body

    def return_user_name(self):
        return User.query.filter_by(id=self.author_id).first().user_name


class Student(db.Model):
    __tabelname__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    first_name = db.Column(db.String(32), nullable=False, index=True)
    middle_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.Enum(gender_enum), nullable=False)
    religion = db.Column(db.Enum(religion_enum), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    student_class = db.Column(db.Enum(student_enum), nullable=False)

    student_courses = db.relationship('Student_Course', backref='student', lazy='dynamic')

    def __init__(self, first_name, middle_name, last_name, gender, religion, date_of_birth, student_class):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.student_class = student_class
        self.religion = religion
        self.date_of_birth = date_of_birth


class Parent(db.Model):
    __tabelname__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    first_name = db.Column(db.String(32), nullable=False, index=True)
    middle_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.Enum(gender_enum), nullable=False)
    parent_class = db.Column(db.Enum(staff_enum), nullable=False)
    religion = db.Column(db.Enum(religion_enum), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    student = db.relationship('Student', backref='parent')

    def __init__(self, first_name, middle_name, last_name, gender, religion, date_of_birth, parent_class):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.parent_class = parent_class
        self.religion = religion
        self.date_of_birth = date_of_birth

    def return_student_user_name(self):
        return User.query.filter_by(id=self.student_id).first().user_name


class Staff(db.Model):
    __tabelname__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    first_name = db.Column(db.String(32), nullable=False, index=True)
    middle_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.Enum(gender_enum), nullable=False)
    staff_class = db.Column(db.Enum(staff_enum), nullable=False)
    religion = db.Column(db.Enum(religion_enum), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    teachers_courses = db.relationship('Student_Course', backref='teacher')

    def __init__(self, first_name, middle_name, last_name, gender, religion, date_of_birth, staff_class):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.gender = gender
        self.staff_class = staff_class
        self.religion = religion
        self.date_of_birth = date_of_birth


class Course(db.Model):
    __tabelname__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    abbreviation = db.Column(db.String(32), nullable=False, unique=True)
    max_score = db.Column(db.Integer)
    success_score = db.Column(db.Integer)

    course_teacher = db.Column(db.String(64))

    added_by = db.Column(db.String(32))
    edited_by = db.Column(db.String(32))

    student_courses = db.relationship('Student_Course', backref='course')

    def __init__(self, name, abbreviation, max_score, success_score, course_teacher, added_by, edited_by):
        self.name = name
        self.abbreviation = abbreviation
        self.max_score = max_score
        self.success_score = success_score
        self.course_teacher = course_teacher
        self.added_by = added_by
        self.edited_by = edited_by

class Student_Course(db.Model):
    __tabelname__ = 'students_courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    student_score = db.Column(db.Integer)

    def __init__(self, student_score):
        self.student_score = student_score
