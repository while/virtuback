from nose.tools import *
from virtuback import app
from flask import json


class TestAPIAdd:
    def setUp(self):
        print('SETUP!')
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        print('TEAR DOWN!')

    def test_update_user_invalid_json(self):
        res = self.client.put('/api/v1.0/user/2', data="not json")
        data = json.loads(res.data)

        assert res.status == '400 BAD REQUEST'
        assert data['message'] == 'Problems parsing JSON'

    def test_update_user_missing_name(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "email": "user3@test.com",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'name', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_update_user_invalid_name(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "",
            "email": "user3@test.com",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'name', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_update_user_missing_email(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "User3",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'email', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_update_user_invalid_email(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "User3",
            "email": "this is an invalid email",
            "password": "thisisavalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'email', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_update_user_missing_password(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "User3",
            "email": "user3@test.com"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'password', 'code': 'missing_field', 'resource': 'User'}
        ]

    def test_update_user_invalid_password(self):
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "User3",
            "email": "user3@test.com",
            "password": "not ok"
        }""", content_type='application/json')
        data = json.loads(res.data)

        print(res.status)
        print(data)
        assert res.status == '422 UNPROCESSABLE ENTITY'
        assert data['message'] == 'Validation Failed'
        assert data['errors'] == [
            {'field': 'password', 'code': 'invalid', 'resource': 'User'}
        ]

    def test_update_user_ok(self):
        """ Test both insert and get of a new user. """
        res = self.client.put('/api/v1.0/user/2', data="""{
            "name": "Newname",
            "email": "thisisnew@test.com",
            "password": "thisisanewvalidpass"
        }""", content_type='application/json')
        data = json.loads(res.data)

        assert res.status == '200 OK'
        assert data['user'] == {
            'id': 2,
            'name': 'Newname',
            'email': 'thisisnew@test.com'
        }
        # test that we have saved the new info in db
        res = self.client.get('/api/v1.0/user/2')
        data = json.loads(res.data)['user']

        assert data['id'] == 2
        assert data['name'] == 'Newname'
        assert data['email'] == 'thisisnew@test.com'
