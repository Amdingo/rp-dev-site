import json
import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username, email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """User Service tests"""

    def test_users(self):
        """Checks /health check route"""
        res = self.client.get('/users/health')
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertIn('healthy', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Add a new user to the database"""
        with self.client:
            res = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'rick',
                    'email': 'rsanchez@randm.com'
                }),
                content_type='application/json',
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertIn('user rick has been created', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_empty(self):
        """If the object is empty, throws an error"""
        with self.client:
            res = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_no_username(self):
        """If there is no username, throws an error"""
        with self.client:
            res = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'rsanchez@randm.com'
                }),
                content_type='application/json',
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_dup_email(self):
        """If the email exists, throws an error"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'rick1',
                    'email': 'rsanchez@randm.com'
                }),
                content_type='application/json',
            )
            res = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'rick2',
                    'email': 'rsanchez@randm.com'
                }),
                content_type='application/json',
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertIn('Sorry, that email address is already in use.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Want a user, get a user"""
        u = add_user('rick', 'rsanchez@randm.com')
        with self.client:
            res = self.client.get(f'/users/{u.id}')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertIn('rick', data['data']['username'])
            self.assertIn('rsanchez@randm.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_no_id(self):
        """no id, get error!"""
        with self.client:
            res = self.client.get('/users/fredflintstone')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_not_exists(self):
        """if id does not exist, get error!"""
        with self.client:
            res = self.client.get('/users/9898')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_users(self):
        """Gets all the users"""
        add_user('rick', 'rsanchez@randm.com')
        add_user('morty', 'msmith@randm.com')
        with self.client:
            res = self.client.get('/users')
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('rick', data['data']['users'][0]['username'])
            self.assertIn('rsanchez@randm.com', data['data']['users'][0]['email'])
            self.assertIn('morty', data['data']['users'][1]['username'])
            self.assertIn('msmith@randm.com', data['data']['users'][1]['email'])


if __name__ == '__main__':
    unittest.main()
