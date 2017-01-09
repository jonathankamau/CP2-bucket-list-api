from flask import Blueprint, request, jsonify
from flask import abort
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer, db
from app.mod_bucketlists.models import BucketList, BucketListItem

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
            abort(403)
    abort(401)


@mod_bucketlists.route('/', methods=['GET', 'POST'])
@auth.login_required
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
    elif request.method == 'POST':
        bucketlist_name = request.form.get('bucket_name')

        if BucketList.query.filter_by(name=bucketlist_name).scalar():
            return jsonify({
                'error': {
                    'message': 'unable to create new bucket list',
                    'details': [
                        {
                            'target': 'bucket_name',
                            'message': 'bucket with same name already exists'
                        }
                    ]
                }
            }), 400

        bucket_list = BucketList(bucketlist_name, user_id)
        bucket_list.save()
        bucket_list.refresh_from_db()

        return jsonify({
            'data': {
                'id': bucket_list.id,
                'name': bucket_list.name,
                'created_by': bucket_list.created_by,
                'date_created': bucket_list.date_created,
                'date_modified': bucket_list.date_modified
            },
            'message': 'new BucketList created successfully'
        }), 201


@mod_bucketlists.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def get_bucketlist(id):
    bucket_list = BucketList.query.filter_by(id=id, created_by=user_id).scalar()

    if not bucket_list:
        return jsonify({
            'error': {
                'message': 'bucket list not found',
                'details': [
                    {
                        'target': 'id',
                        'message': 'BucketList with id provided not found'
                    }
                ]
            }
        }), 404

    if request.method == 'GET':
        bucket_list_items = BucketListItem.query.filter_by(bucketlist_id=bucket_list.id).all()

        return jsonify({
            'data': {
                'id': bucket_list.id,
                'name': bucket_list.name,
                'date_created': bucket_list.date_created,
                'date_modified': bucket_list.date_modified,
                'created_by': bucket_list.created_by,
                'items': [
                    {
                        'id': bucket_list_item.id,
                        'name': bucket_list_item.name,
                        'date_created': bucket_list_item.date_created,
                        'date_modified': bucket_list_item.date_modified,
                        'done': bucket_list_item.done
                    } for bucket_list_item in bucket_list_items
                    ]
            }
        })

    elif request.method == 'PUT':
        new_bucketlist_name = request.form.get('name')

        if not new_bucketlist_name:
            return jsonify({
                'error': {
                    'message': 'unable to create new bucket list item',
                    'details': [
                        {
                            'target': 'name',
                            'message': 'name data field missing/empty from POST request'
                        }
                    ]
                }
            }), 400

        if new_bucketlist_name == bucket_list.name:
            return jsonify({
                'error': {
                    'message': 'new BucketList name is equal to new name',
                    'details': [
                        {
                            'target': 'name',
                            'message': 'new BucketList name is equal to new name'
                        }
                    ]
                }
            }), 400

        bucket_list.name = new_bucketlist_name
        bucket_list.save()
        bucket_list.refresh_from_db()

        return jsonify({
            'data': {
                'id': bucket_list.id,
                'name': bucket_list.name,
                'date_created': bucket_list.date_created,
                'date_modified': bucket_list.date_modified,
                'created_by': bucket_list.created_by
            },
            'message': 'updated bucketlist name'
        })

    elif request.method == 'DELETE':

        BucketList.query.filter_by(id=id, created_by=user_id).delete()
        db.session.commit()

        if not BucketList.query.filter_by(id=id, created_by=user_id).scalar():
            return jsonify({
                'data': {
                    'message': 'successfully deleted bucketlist'
                }
            })


@mod_bucketlists.route('/<id>/items/', methods=['POST'])
@auth.login_required
def create_bucketlist_item(id):
    bucket_list = BucketList.query.filter_by(id=id, created_by=user_id).scalar()

    if not bucket_list:
        return jsonify({
            'error': {
                'message': 'bucketlist list does not exists'
            }
        }), 404

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            return jsonify({
                'error': {
                    'message': 'unable to create bucketlist item',
                    'details': [
                        {
                            'target': 'name',
                            'message': 'name data field missing/empty from POST request'
                        }
                    ]
                }
            }), 400

        bucketlist_item = BucketListItem.query.filter_by(name=name).all()

        if bucketlist_item:
            return jsonify({
                'error': {
                    'message': 'cannot create bucketlist item'
                }
            }), 403

        bucketlist_item = BucketListItem(name, description, bucket_list.id)
        bucketlist_item.save()
        bucketlist_item.refresh_from_db()

        return jsonify({
            'message': 'successfully created bucketlist items',
            'data': {
                'id': bucketlist_item.id,
                'name': bucketlist_item.name,
                'description': bucketlist_item.description,
                'date_created': bucketlist_item.date_created,
                'date_modified': bucketlist_item.date_modified,
                'done': bucketlist_item.done
            }
        }), 201


@mod_bucketlists.route('/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
@auth.login_required
def modify_bucketlist_item(id, item_id):
    bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=id, id=item_id).scalar()

    if not bucketlist_item:
        return jsonify({
            'error': {
                'message': 'bucketlist item not found'
            }
        }), 404

    if request.method == 'PUT':
        bucketlist_item.name = request.form.get('name', bucketlist_item.name)
        bucketlist_item.done = request.form.get('done', bucketlist_item.done)
        bucketlist_item.description = request.form.get('description', bucketlist_item.description)

        bucketlist_item.save()
        bucketlist_item.refresh_from_db()

        return jsonify({
            'message': 'successfully updated bucketlist item',
            'data': {
                'id': bucketlist_item.id,
                'name': bucketlist_item.name,
                'description': bucketlist_item.description,
                'date_created': bucketlist_item.date_created,
                'date_modified': bucketlist_item.date_modified,
                'done': bucketlist_item.done
            }

        })
