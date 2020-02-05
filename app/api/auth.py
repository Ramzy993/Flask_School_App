from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_tokken, password):
    if email_or_tokken == '':
        return False
    if password == '':
        g.current_user = User.verify_user_token(email_or_tokken)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_tokken).first()
    if not user:
        return False

    g.current_user = user
    g.token_used = False


@api.before_request
@auth.login_required
def before_request():
    if g.current_user.is_anonymous and not g.curren_user.is_confirmed:
        return forbidden('Unconfirmed Account')


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
