from flask import jsonify, abort, request, make_response
from hashlib import sha256
import re
import copy
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
        user = next(search)
    except StopIteration:
        abort(404)

    user_copy = copy.deepcopy(user)
    del user_copy['password']

    return jsonify({'user': user_copy}), 200


# ------------------------------------------------------------------------------
#  POST route to insert a new user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/users', methods=['POST'])
def insert_user():
    # Do we get valid JSON in the request?
    if not request.json:
        abort_with_reason(jsonify({"message": "Problems parsing JSON"}), 400)

    # Validate required input fields in JSON
    errors = validate_fields(request.json)
    if len(errors) > 0:
        abort_with_reason(jsonify({'message': 'Validation Failed',
                                   'errors': errors}), 422)
    # Create new user from request
    new = {
        'id': len(users) + 1,
        'name': request.json['name'],
        'email': request.json['email'],
        'password': sha256(request.json['password'].encode('UTF-8')).hexdigest()
    }
    users.append(new)

    # Respond with an object copy without password field
    user_copy = copy.deepcopy(new)
    del user_copy['password']

    return jsonify({'user': user_copy}), 201


# ------------------------------------------------------------------------------
#  PUT route to update a user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['PUT'])
def update_user(id):
    # Do we get valid JSON?
    if not request.json:
        abort_with_reason(jsonify({"message": "Problems parsing JSON"}), 400)

    # Validate requires fields in request
    errors = validate_fields(request.json)
    if len(errors) > 0:
        abort_with_reason(jsonify({'message': 'Validation Failed',
                                   'errors': errors}), 422)

    # Does the user we want to update exist?
    search = filter(lambda d: d['id'] == id, users)
    try:
        user = next(search)
    except StopIteration:
        # If not there return 404 not found
        abort(404)

    # Update the fields
    user['name'] = request.json['name']
    user['email'] = request.json['email']
    user['password'] = sha256(request.json['password'].encode('UTF-8')).hexdigest()

    # Return JSON object without password
    user_copy = copy.deepcopy(user)
    del user_copy['password']

    return jsonify({'user': user_copy}), 200


# -------------------------------------------------------------------------------
#  DELETE route to remove a user resource
# -------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['DELETE'])
def remove_user(id):
    # Does the user we want to update exist?
    search = filter(lambda d: d['id'] == id, users)
    try:
        user = next(search)
    except StopIteration:
        # If not there return 404 not found
        abort(404)

    # Remove the requested id. no fuzz
    del users[id - 1]

    # Return empty 200 OK message
    return '', 200


# -------------------------------------------------------------------------------
#  Function for field validation
# -------------------------------------------------------------------------------
def validate_fields(data):
    errors = []
    if 'name' not in data:
        errors.append({
            'resource': 'User',
            'field': 'name',
            'code': 'missing_field'
        })
    elif data['name'] == '':
        errors.append({
            'resource': 'User',
            'field': 'name',
            'code': 'invalid'
        })

    if 'email' not in data:
        errors.append({
            'resource': 'User',
            'field': 'email',
            'code': 'missing_field'
        })
    elif not re.match('^[^@\s]+@[^@\s]+\.[a-zA-Z]+$', data['email']):
        errors.append({
            'resource': 'User',
            'field': 'email',
            'code': 'invalid'
        })

    if 'password' not in data:
        errors.append({
            'resource': 'User',
            'field': 'password',
            'code': 'missing_field'
        })
    elif len(data['password']) < 8:
        errors.append({
            'resource': 'User',
            'field': 'password',
            'code': 'invalid'
        })

    return errors


# ------------------------------------------------------------------------------
#  Send abort response with a reason
# ------------------------------------------------------------------------------
def abort_with_reason(response, code):
    response = make_response(response)
    response.status_code = code
    #response.headers = {"X-Status-Reason": message}
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
