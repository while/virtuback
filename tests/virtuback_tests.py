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
        res = self.client.get('/api/v1.0/nottobefound')
        assert res.status == "404 NOT FOUND"

    def test_user_get(self):
        res = self.client.get('/api/v1.0/user/1')
        data = json.loads(res.data)['user']
        print(data)
        assert data['id'] == 1
        assert data['name'] == u'Vilhelm von Ehrenheim'
        assert data['email'] == u'vonehrenheim@gmail.com'
