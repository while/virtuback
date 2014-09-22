from flask import jsonify
from virtuback import app


users = [
    {
        'id':        1,
        'name':      u"Vilhelm von Ehrenheim",
        'email':     u"vonehrenheim@gmail.com",
        'password':  u"abc123"
    },
    {
        'id':        2,
        'name':      u"Tester Testsson",
        'email':     u"test@test.com",
        'password':  u"qwerty"
    },
]


# Set up GET listing of all users !!UNSAFE?
@app.route('/api/v1.0/users', methods=['GET'])
def list_users():
    return jsonify({'users': users})
