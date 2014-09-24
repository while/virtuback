from nose.tools import *
from virtuback import app
from virtuback import db
from flask import json
from hashlib import sha256


class TestPOST:
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

    def test_add_user_invalid_json(self):
        res = self.client.post('/api/v1.0/users', data="not json")
        data = json.loads(res.data)

        assert res.status == '400 BAD REQUEST'
        assert data['message'] == 'Problems parsing JSON'

    def test_add_user_missing_name(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "email": "valid@email.com",
            "password": "validpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'name', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_add_user_empty_name(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "",
            "email": "valid@email.com",
            "password": "validpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'name', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_add_user_missing_email(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tester",
            "password": "validpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'email', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_add_user_empty_email(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tester",
            "email": "",
            "password": "validpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'email', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_add_user_invalid_email(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tester",
            "email": "invalid_email",
            "password": "validpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'email', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_add_user_missing_pwd(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tester",
            "email": "valid@email.com"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'password', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_add_user_invalid_pwd(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "Tester",
            "email": "valid@email.com",
            "password": "invalid"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'password', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_add_user_invalid_all(self):
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "",
            "email": "invalid_email",
            "password": "invalid"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'name', 'code': 'invalid', 'resource': 'User'},
            {'field': 'email', 'code': 'invalid', 'resource': 'User'},
            {'field': 'password', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_add_user_ok(self):
        """ Test both insert and get of a new user. """
        res = self.client.post('/api/v1.0/users', data="""{
            "name": "User3",
            "email": "user3@test.com",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '201 CREATED'
        assert data['user'] == {
            'id': 3,
            'name': 'User3',
            'email': 'user3@test.com'
        }
        # test that we have it in db now
        data = self.db.find_one({'_id': 3})

        assert data['name'] == u'User3'
        assert data['email'] == u'user3@test.com'
