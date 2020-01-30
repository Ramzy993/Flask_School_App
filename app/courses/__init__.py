from flask import Blueprint

courses_blueprint = Blueprint('courses', __name__)

from . import views
