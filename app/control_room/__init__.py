from flask import Blueprint

control_room_blueprint = Blueprint('control_room', __name__)

from . import views
from ..models import Permission


@control_room_blueprint.app_context_processor
def inject_permission():
    return dict(Permission=Permission)