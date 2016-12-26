from flask import Blueprint

mod_bucketlists = Blueprint('bucketlists', __name__, url_prefix='/bucketlists')


@mod_bucketlists.route('/', methods=['GET', 'POST'])
def get_bucketlists():
    pass


@mod_bucketlists.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_bucketlist(id):
    pass


@mod_bucketlists.route('<id>/items/', methods=['POST'])
def create_bucketlist_item(id):
    pass


@mod_bucketlists.route('<id>/items/<item_id>', methods=['PUT', 'DELETE'])
def modify_bucketlist_item(id, item_id):
    pass
