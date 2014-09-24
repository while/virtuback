from nose.tools import *
from virtuback import app
from virtuback import db
from flask import json
from hashlib import sha256


class SetupAPI:
    def setUp(self):
        print('SETUP!')
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.db = db._client.virtuback_test.users
        self.db.insert({
            '_id':       1,
            'name':     'Vilhelm von Ehrenheim',
            'email':    'vonehrenheim@gmail.com',
            'password': sha256(b'abc123').hexdigest()
        })
        self.db.insert({
            '_id':       2,
            'name':     'Tester Testsson',
            'email':    'test@test.com',
            'password': sha256(b'qwerty').hexdigest()
        })

    def tearDown(self):
        print('TEAR DOWN!')
        self.db.remove()


class TestGET(SetupAPI):
    def test_404(self):
        res = self.client.get('/api/v1.0/nevertobefound')
        assert res.status == "404 NOT FOUND"

    def test_get_user_not_there(self):
        res = self.client.get('/api/v1.0/user/0')
        assert res.status == "404 NOT FOUND"

    def test_get_user_ok(self):
        res = self.client.get('/api/v1.0/user/1')
        print(res.data)
        data = json.loads(res.data)['user']

        assert data['id'] == 1
        assert data['name'] == 'Vilhelm von Ehrenheim'
        assert data['email'] == 'vonehrenheim@gmail.com'

class TestDELETE(SetupAPI):
    def test_delete_user_not_there(self):
        res = self.client.delete('/api/v1.0/user/0')
        assert res.status == "404 NOT FOUND"

    def test_delete_user_ok(self):
        # Add a user we can remove
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tmp",
            "email": "tmp@test.com",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)['user']

        res = self.client.delete('/api/v1.0/user/' + str(data['id']))
        assert res.status == "200 OK"

        res = self.client.get('/api/v1.0/user/' + str(data['id']))
        assert res.status == "404 NOT FOUND"
