import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import app


class TestDevConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevConfig')
        return app

    def test_app_is_dev(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )


class TestTestConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestConfig')
        return app

    def test_app_is_test(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('TEST_DATABASE_URL')
        )


class TestProdConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProdConfig')
        return app

    def test_app_is_prod(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
