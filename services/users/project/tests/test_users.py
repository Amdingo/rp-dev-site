import json
import unittest

from project.tests.base import BaseTestCase


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


if __name__ == '__main__':
    unittest.main()
