from flask import jsonify, abort, request, make_response
from hashlib import sha256
import re
from virtuback import app


# Define a mock users db
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


# ------------------------------------------------------------------------------
#  Set up GET listing of all users !!UNSAFE?
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/users', methods=['GET'])
def list_users():
    """ Method for listing all users via GET request. """
    all = [{'id': d['id'], 'name': d['name'], 'email': d['email']} for d in users]
    return jsonify({'users': all})


# ------------------------------------------------------------------------------
#  GET route for single user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['GET'])
def get_user(id):
    search = filter(lambda d: d['id'] == id, users)
    try:
        return jsonify({'user': next(search)})
    except StopIteration:
        abort(404)


# ------------------------------------------------------------------------------
#  POST route to insert a new user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/users', methods=['POST'])
def insert_user(id):
    if not request.json:
        abort(400)

    if 'name' not in request.json or request.json['name'] == '':
        abort_with_reason('Invalid name', 400)

    if ('email' not in request.json or
        not re.match('^[^@\s]+@[^@\s]+\.[a-zA-Z]+$', request.json['email'])):
        abort_with_reason('Invalid email', 400)

    if 'password' not in request.json or len(request.json['password']) < 8:
        abort_with_reason('Password too short! Must be >= 8 characters.', 400)

    new = {
        'id': len(users) + 1,
        'name': request.json['name'],
        'email': request.json['email'],
        'password': sha256(request.json['password'].encode('UTF-8')).hexdigest()
    }
    users.append(new)

    return jsonify({'user': new}), 201


# ------------------------------------------------------------------------------
#  PUT route to update a user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['PUT'])
def update_user(id):
    search = filter(lambda d: d['id'] == id, users)
    try:
        user = search.next()
    except StopIteration:
        abort(404)
    abort(501)


# -------------------------------------------------------------------------------
#  DELETE route to remove a user
# -------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['DELETE'])
def remove_user(id):
    abort(501)


# ------------------------------------------------------------------------------
#  Send abort response with a reason
# ------------------------------------------------------------------------------
def abort_with_reason(reason, code):
    response = make_response(jsonify({'error': reason}))
    response.status_code = code
    response.headers = {"X-Status-Reason": reason}
    abort(response)


# ------------------------------------------------------------------------------
#  404 not found response
# ------------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': '404 NOT FOUND'}), 404)


# ------------------------------------------------------------------------------
#  501 not implemented response
# ------------------------------------------------------------------------------
@app.errorhandler(501)
def not_implemented(error):
        return make_response(jsonify({'error': '501 NOT IMPLEMENTED'}), 501)
