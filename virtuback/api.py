from flask import jsonify, abort, request, make_response
from hashlib import sha256
import re
import copy
from virtuback import app
from virtuback import db


# ------------------------------------------------------------------------------
#  Set up GET listing of all users !!UNSAFE?
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/users', methods=['GET'])
def list_users():
    """ Method for listing all users via GET request. """
    all = []
    for u in db.users().find():
        all.append({
            'id': int(u['_id']),
            'name': u['name'],
            'email': u['email'],
        })
    return jsonify({'users': all})


# ------------------------------------------------------------------------------
#  GET route for single user
# ------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['GET'])
def get_user(id):
    user = db.users().find_one({'_id': id})

    if user is None:
        abort(404)

    return jsonify({
        'user': {
            'id': int(user['_id']),
            'name': user['name'],
            'email': user['email'],
        }
    }), 200


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
        '_id': db.users().find().count() + 1,
        'name': request.json['name'],
        'email': request.json['email'],
        'password': sha256(request.json['password'].encode('UTF-8')).hexdigest()
    }
    db.users().insert(new)

    # Respond with a user object without password field
    return jsonify({
        'user': {
            'id': int(new['_id']),
            'name': new['name'],
            'email': new['email'],
        }
    }), 201


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
    user = db.users().find_one({'_id': id})
    if user is None:
        abort(404)

    # Update the fields
    upd = {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': sha256(request.json['password'].encode('UTF-8')).hexdigest()
    }

    db.users().update({'_id': id}, upd)

    # Return JSON object without password
    upd['id'] = id
    del upd['password']

    return jsonify({'user': upd}), 200


# -------------------------------------------------------------------------------
#  DELETE route to remove a user resource
# -------------------------------------------------------------------------------
@app.route('/api/v1.0/user/<int:id>', methods=['DELETE'])
def remove_user(id):
    ret = db.users().remove({'_id': id})
    # Does the user we want to update exist?
    if ret['n'] == 0:
        abort(404)

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
        return make_response(jsonify({'message': 'Not Found'}), 404)


# ------------------------------------------------------------------------------
#  501 not implemented response
# ------------------------------------------------------------------------------
@app.errorhandler(501)
def not_implemented(error):
        return make_response(jsonify({'message': 'Not Implemented'}), 501)
