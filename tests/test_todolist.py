import unittest
import os
import json
from app import create_app, db


class TodolistTestCase(unittest.TestCase):
    """This class represents the todolist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.todolist = {'name': 'test1231321'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_todolist_creation(self):
        """Test API can create a todolist (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.todolist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('test123', str(res.data))

    def test_api_can_get_all_todolists(self):
        """Test API can get a todolist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.todolist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('test123', str(res.data))

    def test_api_can_get_todolist_by_id(self):
        """Test API can get a single todolist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.todolist)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())
        result = self.client().get(
            '/todolists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('test123', str(result.data))

    def test_todolist_can_be_edited(self):
        """Test API can edit an existing todolist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'abc'})
        self.assertEqual(rv.status_code, 201)
        # get the json with the todolist
        results = json.loads(rv.data.decode())
        rv = self.client().put(
            '/todolists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "def"
            })

        self.assertEqual(rv.status_code, 200)
        results = self.client().get(
            '/todolists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('def', str(results.data))

    def test_todolist_deletion(self):
        """Test API can delete an existing todolist. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/todolists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': '123abc'})
        self.assertEqual(rv.status_code, 201)
        # get the todolist in json
        results = json.loads(rv.data.decode())
        res = self.client().delete(
            '/todolists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/todolists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
