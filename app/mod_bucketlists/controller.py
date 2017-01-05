from flask import Blueprint, request, jsonify
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer
from app.mod_bucketlists.models import BucketList

mod_bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')
auth = HTTPTokenAuth('Token')

user_id = 1

@auth.verify_token
def verify_token(token):
    """Receives token and verifies it, the username and time_created
     must return True or False"""
    if token:  # TODO fix the token validation clause
        try:
            user_name, time_created = token_signer.unsign(token, return_timestamp=True)  # TODO get user id
            return True
        except (BadTimeSignature, BadSignature)as e:
            return True  # TODO return message on token failure

    return False


@mod_bucketlists.route('/', methods=['GET', 'POST'])
def get_bucketlists():
    if request.method == 'GET':
        bucket_lists = BucketList.query.filter_by(created_by=user_id).all()

        return jsonify({
            'data': [
                {
                    'id': bucket_list.id,
                    'name': bucket_list.name,
                    'created_by': bucket_list.created_by,
                    'date_created': bucket_list.date_created,
                    'date_modified': bucket_list.date_modified
                } for bucket_list in bucket_lists
                ]
        })
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
