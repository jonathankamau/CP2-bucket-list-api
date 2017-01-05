# encoding: utf-8
from flask import Blueprint, jsonify
from flask import request

from app.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/register/', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return jsonify({
            'error': {
                'message': 'unable to create user',
                'details': [
                    {
                        'target': 'username',
                        'message': 'username data field missing/empty from POST request'
                    }
                ]
            }
        }), 400

    if not password:
        return jsonify({
            'error': {
                'message': 'unable to create user',
                'details': [
                    {
                        'target': 'password',
                        'message': 'password data field missing/empty from POST request'
                    }
                ]
            }
        }), 400

    if User.query.filter_by(username=username).scalar():
        return jsonify({
            'error': {
                'message': 'unable to create user',
                'details': [
                    {
                        'target': 'username',
                        'message': 'username already registered'
                    }
                ]
            }
        }), 400

    user = User(username, password)
    user.save()
    user.refresh_from_db()

    return jsonify({
        'data': {
            'username': user.username,
            'message': 'new user created successfully'
        }
    }), 201


@mod_auth.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username:
        return jsonify({
            'error': {
                'message': 'unable to login user',
                'details': [
                    {
                        'target': 'username',
                        'message': 'username data field missing/empty from POST request'
                    }
                ]
            }
        }), 400

    if not password:
        return jsonify({
            'error': {
                'message': 'unable to login user',
                'details': [
                    {
                        'target': 'password',
                        'message': 'password data field missing/empty from POST request'
                    }
                ]
            }
        }), 400

    user = User.query.filter_by(username=username).first()

    if user and user.verify_password_hash(password):
        return jsonify({
            'data': {
                'message': 'login successful. Use token for authentication for the API',
                'username': user.username,
                'token': str(user.token)
            }
        })

    return jsonify({
        'error': {
            'message': 'invalid username/password combination'
        }
    }), 401
