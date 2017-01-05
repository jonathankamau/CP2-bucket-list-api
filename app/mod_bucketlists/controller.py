from flask import Blueprint
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer

mod_bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')
auth = HTTPTokenAuth('Token')


@auth.verify_token
def verify_token(token):
    """Receives token and verifies it, the username and time_created
     must return True or False"""
    if token:  # TODO fix the token validation clause
        try:
            user_name, time_created = token_signer.unsign(token, return_timestamp=True)
        except (BadTimeSignature, BadSignature)as e:
            return False
        return True
    return False


@mod_bucketlists.route('/', methods=['GET', 'POST'])
@auth.verify_token
def get_bucketlists():
    return "not implmented"


@mod_bucketlists.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_bucketlist(id):
    return "not implmented"


@mod_bucketlists.route('/<id>/items/', methods=['POST'])
def create_bucketlist_item(id):
    return "not implmented"


@mod_bucketlists.route('/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
def modify_bucketlist_item(id, item_id):
    return "not implmented"
