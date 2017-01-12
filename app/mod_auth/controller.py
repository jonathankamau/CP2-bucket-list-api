# encoding: utf-8
from flask import Blueprint, jsonify, abort, request

from app import app
from app.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

"""
provides the routes to register and login a user. It also display the token for API
"""


@app.errorhandler(401)
def custom401error(exception):
    return jsonify(exception.description), 401


@app.errorhandler(400)
def custom400error(exception):
    return jsonify(exception.description), 400


@mod_auth.route('/register/', methods=['POST'])
def register():
    """
    Creates a new user when provided username and password via POST
    Returns: JSON response with status of register user
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return abort(400, {
            'error': {
                'message': 'username data field missing/empty from POST request'
            }
        })

    if not password:
        abort(400, {
            'error': {
                'message': 'password data field missing/empty from POST request'
            }
        })

    if User.query.filter_by(username=username).scalar():
        abort(400, {
            'error': {
                'message': 'username already registered'
            }
        })

    user = User(username, password)
    user.save()
    user.refresh_from_db()

    return jsonify({
        'username': user.username,
        'message': 'new user created successfully'
    }), 201


@mod_auth.route('/login/', methods=['POST'])
def login():
    """
    validate the username and password supplied via POST to authenticate the user
    Returns:
        JSON response with username, and token
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        abort(400, {
            'error': {
                'message': 'username data field missing/empty from POST request'
            }
        })

    if not password:
        abort(400, {
            'error': {
                'message': 'password data field missing/empty from POST request'
            }

        })

    user = User.query.filter_by(username=username).first()

    if user and user.verify_password_hash(password):
        return jsonify({
            'message': 'login successful. Use token for authentication for the API',
            'username': user.username,
            'token': user.token.decode()
        })

    abort(401, {
        'error': {
            'message': 'invalid username/password combination'
        }
    })
