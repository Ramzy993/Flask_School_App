from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(sum(Permission.roles['Administrator']))(f)


def management_required(f):
    return permission_required(sum(Permission.roles['Management']))(f)


def teacher_required(f):
    return permission_required(sum(Permission.roles['Teacher']))(f)


def parent_required(f):
    return permission_required(sum(Permission.roles['Parent']))(f)


def student_required(f):
    return permission_required(sum(Permission.roles['Student']))(f)
