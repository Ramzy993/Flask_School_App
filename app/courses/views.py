from flask import render_template, redirect, request, url_for, flash, session
from ..decorators import permission_required, admin_required
from flask import render_template
from flask_login import login_user, logout_user, login_required, current_user
from . import courses_blueprint
from ..models import User, Permission


@courses_blueprint.route('/view_courses')
@login_required
@permission_required(Permission.VIEW_COURSES)
def view_courses():
    return redirect(url_for('main.index'))


@courses_blueprint.route('/edit_courses')
@login_required
@permission_required(Permission.EDIT_COURSES)
def edit_courses():
    return redirect(url_for('main.index'))
