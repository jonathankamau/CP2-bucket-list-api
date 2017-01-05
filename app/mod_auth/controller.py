# encoding: utf-8
from flask import Blueprint, jsonify
from flask import request

from app.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/register/', methods=['POST'])
def register():
    username = request.form.get('username')

    if User.query.filter_by(username=username).scalar():
        return jsonify({
            'error': {
                'message': 'unable to create user',
                'details': 'username already registered'
            }
        }), 400

    password = request.form.get('password')
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
    return ""
