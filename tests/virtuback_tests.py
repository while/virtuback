from nose.tools import *
from virtuback import app
from flask import json

class TestAPI:
    def setUp(self):
        print('SETUP!')
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        print('TEAR DOWN!')

    def test_404(self):
        res = self.client.get('/api/v1.0/nevertobefound')
        assert res.status == "404 NOT FOUND"

    def test_get_user_not_there(self):
        res = self.client.get('/api/v1.0/user/0')
        assert res.status == "404 NOT FOUND"

    def test_get_user_ok(self):
        res = self.client.get('/api/v1.0/user/1')
        data = json.loads(res.data)['user']

        assert data['id'] == 1
        assert data['name'] == u'Vilhelm von Ehrenheim'
        assert data['email'] == u'vonehrenheim@gmail.com'

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
