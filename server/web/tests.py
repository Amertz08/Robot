import unittest

from flask import url_for
from flask_testing import TestCase

from factory import create_app
from models import db, User, Account

class BaseTest(TestCase):

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestMain(BaseTest):

    def test_index(self):
        resp = self.client.get(url_for('main.index'))
        self.assert200(resp)

if __name__ == '__main__':
    unittest.main()
