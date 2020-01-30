from flask import Blueprint

managements_blueprint = Blueprint('managements', __name__)

from . import views
