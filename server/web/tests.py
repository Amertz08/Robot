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

    @staticmethod
    def add_acct(company_name):
        acct = Account(company_name=company_name)
        db.session.add(acct)
        db.session.commit()
        return acct

    @staticmethod
    def add_user(acct_id, first, last, email, password):
        user = User(
            acct_id=acct_id,
            first_name=first,
            last_name=last,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return user

class TestMain(BaseTest):

    def test_index(self):
        resp = self.client.get(url_for('main.index'))
        self.assert200(resp)
        self.assert_template_used('main/index.html.j2')


class TestAuth(BaseTest):

    def test_login_basic(self):
        resp = self.client.get(url_for('auth.login'))
        self.assert200(resp)
        self.assert_template_used('auth/login.html.j2')
        self.assertIn(b'<h1>Login</h1>', resp.data, 'Title missing')
        self.assertIn(b'>Reset Password</a>', resp.data, 'Reset password link missing')

    def test_login_no_user(self):
        data = {
            'email': 'adam@example.com',
            'password': 'pass'
        }
        resp = self.client.post(url_for('auth.login'), data=data)
        self.assert200(resp)
        self.assertIn(b'Invalid Email/Password', resp.data)

    def test_login_valid_user_invalid_pw(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        data = {
            'email': 'adam@example.com',
            'password': 'wrong'
        }

        resp = self.client.post(url_for('auth.login'), data=data)
        self.assert200(resp)
        self.assertIn(b'Invalid Email/Password', resp.data)

    def test_login_valid_user_valid_pw_no_follow(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        data = {
            'email': 'adam@example.com',
            'password': 'pass'
        }

        resp = self.client.post(url_for('auth.login'), data=data)
        self.assertRedirects(resp, url_for('main.index'), 'Should redirect to main.index')

    def test_login_valid_user_valid_pw_follow(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        data = {
            'email': 'adam@example.com',
            'password': 'pass'
        }

        resp = self.client.post(url_for('auth.login'), data=data, follow_redirects=True)
        self.assert200(resp)
        self.assertIn(b'Login Successful', resp.data, 'Login Successful message missing')
        self.assertIn(b'Logout</a>', resp.data, 'Logout link should appear')
        self.assertNotIn(b'Login</a>', resp.data, 'Login link should not appear')



if __name__ == '__main__':
    unittest.main()
