from flask import Blueprint

results_blueprint = Blueprint('results', __name__)

from . import views