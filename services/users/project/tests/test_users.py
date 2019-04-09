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


if __name__ == '__main__':
    unittest.main()
