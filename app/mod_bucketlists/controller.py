from flask import Blueprint, request, jsonify, abort
from flask import url_for
from flask_httpauth import HTTPTokenAuth
from itsdangerous import BadTimeSignature, BadSignature

from app import token_signer, db, app
from app.mod_auth.models import User
from app.mod_bucketlists.models import BucketList, BucketListItem

"""
Creates the bucketlist and manipulates the items in  the bucketlist
"""

mod_bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')
auth = HTTPTokenAuth('Token')

user_id = None


@app.errorhandler(401)
def custom401(error):
    return jsonify(error.description), 401


@app.errorhandler(403)
def custom400(error):
    return jsonify(error.description), 403


@auth.verify_token
def verify_token(token):
    """Receives token and verifies it, the username
     must return True or error response"""
    if token:
        try:
            user_name = token_signer.unsign(token)

            user = User.query.filter_by(username=user_name.decode()).scalar()

            if user:
                global user_id
                user_id = user.id

                if token != user.token.decode():
                    abort(403, {
                        'error': {
                            'message': 'expired token supplied'
                        }
                    })

                return True
        except (BadTimeSignature, BadSignature):
            abort(403, {
                'error': {
                    'message': 'invalid token supplied'
                }
            })

    return abort(401, {
        'error': {
            'message': 'no token to submitted'
        }
    })


@mod_bucketlists.route('/', methods=['GET', 'POST'])
@auth.login_required
def get_bucketlists():
    """
    Creates and views the bucketlist
    Returns:
        JSON file with the bucketlist, 201 on create and 200 on retrieve
    """
    if request.method == 'GET':

        page_no = request.args.get('pag_no', 1)
        limit = request.args.get('limit', 20)
        search_name = request.args.get('q', '')

        bucket_lists = BucketList.query.filter_by(created_by=user_id) \
            .filter(BucketList.name.like('%{}%'.format(search_name))) \
            .paginate(int(page_no), int(limit))

        return jsonify({
            'data': [
                {
                    'id': bucket_list.id,
                    'name': bucket_list.name,
                    'created_by': bucket_list.created_by,
                    'date_created': bucket_list.date_created,
                    'date_modified': bucket_list.date_modified
                } for bucket_list in bucket_lists.items

                ],
            'next': '{}?q={}&limit={}&page={}'.format(
                str(url_for('bucketlists.get_bucketlists', _external=True)),
                str(search_name),
                str(limit),
                str(page_no + 1)) if bucket_lists.has_next else None,
            'prev': '{}?q={}&limit={}&page={}'.format(
                str(url_for('bucketlists.get_bucketlists', _external=True)),
                str(search_name),
                str(limit),
                str(page_no - 1)) if bucket_lists.has_prev else None
        })
    elif request.method == 'POST':
        bucketlist_name = request.form.get('bucket_name')

        if BucketList.query.filter_by(name=bucketlist_name).scalar():
            return abort(400, {
                'error': {
                    'message': 'bucket with same name already exists'
                }

            })

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
            }
        }), 201


@mod_bucketlists.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def get_bucketlist(id):
    """
    Get a single bucketlist and items if available. It allows manipulate the bucketlist details
    Args:
        id: The id of the bucketlist

    Returns:
        JSON files with bucketlists details and items; 200 on successfully request
    """
    bucket_list = BucketList.query.filter_by(id=id, created_by=user_id).scalar()

    if not bucket_list:
        return jsonify({
            'error': {
                'message': 'bucket list not found'
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
            return abort(400, {
                'error': {
                    'message': 'name data field missing/empty from POST request'
                }

            })

        if new_bucketlist_name == bucket_list.name:
            return abort(403, {
                'error': {
                    'message': 'new BucketList name is equal to new name'

                }
            })

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
            }
        })

    elif request.method == 'DELETE':

        BucketList.query.filter_by(id=id, created_by=user_id).delete()
        db.session.commit()

        if not BucketList.query.filter_by(id=id, created_by=user_id).scalar():
            return jsonify({
                'message': 'successfully deleted bucketlist'
            })


@mod_bucketlists.route('/<id>/items/', methods=['POST'])
@auth.login_required
def create_bucketlist_item(id):
    """
    Creates a new item in the bucketlist
    Args:
        id: the bucketlist id to create the item in

    Returns:
        JSON file with details of created bucketlist item; 201 on succeful request

    """
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
            return abort(400, {
                'error': {
                    'message': 'name data field missing/empty from POST request'
                }

            })

        bucketlist_item = BucketListItem.query.filter_by(name=name).all()

        if bucketlist_item:
            return abort(403, {
                'error': {
                    'message': 'cannot create bucketlist item'
                }
            })

        bucketlist_item = BucketListItem(name, description, bucket_list.id)
        bucketlist_item.save()
        bucketlist_item.refresh_from_db()

        return jsonify({
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
    """
    Updates or deletes the bucketlist items
    Args:
        id: bucketlist id
        item_id:  bucketlist item id

    Returns:
        JSON file with the details of the modified bucketlist item; 200 on successful request

    """
    bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=id, id=item_id).scalar()

    if not bucketlist_item:
        return jsonify({
            'error': {
                'message': 'bucketlist item not found'
            }
        }), 404

    if request.method == 'PUT':
        done_status = request.form.get('done', '').lower()
        if done_status and done_status not in ('true', 'false'):
            return abort(400, {
                'error': {
                    'message': 'done status should be true or false'
                }
            })

        bucketlist_item.name = request.form.get('name', bucketlist_item.name)
        bucketlist_item.done = done_status == 'true'
        bucketlist_item.description = request.form.get('description', bucketlist_item.description)

        bucketlist_item.save()
        bucketlist_item.refresh_from_db()

        return jsonify({
           'data': {
                'id': bucketlist_item.id,
                'name': bucketlist_item.name,
                'description': bucketlist_item.description,
                'date_created': bucketlist_item.date_created,
                'date_modified': bucketlist_item.date_modified,
                'done': bucketlist_item.done
            }

        })
