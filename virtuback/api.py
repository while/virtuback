from flask import jsonify, abort, make_response
from hashlib import sha256
from virtuback import app


# Define a mock users list
users = [
    {
        'id':        1,
        'name':      u'Vilhelm von Ehrenheim',
        'email':     u'vonehrenheim@gmail.com',
        'password':  sha256(b'abc123').hexdigest()
    },
    {
        'id':        2,
        'name':      u'Tester Testsson',
        'email':     u'test@test.com',
        'password':  sha256(b'qwerty').hexdigest()
    },
]


# Set up GET listing of all users !!UNSAFE?
@app.route('/api/v1.0/users', methods=['GET'])
def list_users():
    """ Method for listing all users via GET request. """
    all = [{'id': d['id'], 'name': d['name'], 'email': d['email']} for d in users]
    return jsonify({'users': all})


# GET route for single user
@app.route('/api/v1.0/user/<int:id>', methods=['GET'])
def get_user(id):
    search = filter(lambda d: d['id'] == id, users)
    try:
        return jsonify({'user': next(search)})
    except StopIteration:
        abort(404)


# POST route to insert a new user
@app.route('/api/v1.0/user/<int:id>', methods=['POST'])
def insert_user(id):
    abort(501)


# PUT route to update a user
@app.route('/api/v1.0/user/<int:id>', methods=['PUT'])
def update_user(id):
    abort(501)


# DELETE route to remove a user
@app.route('/api/v1.0/user/<int:id>', methods=['DELETE'])
def remove_user(id):
    abort(501)


@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': '404 NOT FOUND'}), 404)


@app.errorhandler(501)
def not_implemented(error):
        return make_response(jsonify({'error': '501 NOT IMPLEMENTED'}), 501)
