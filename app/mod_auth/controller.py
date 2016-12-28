from flask import Blueprint

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    pass


@mod_auth.route('/login', methods=['POST'])
def login():
    pass
