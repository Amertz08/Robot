import datetime
import unittest

from flask import url_for
from flask_testing import TestCase
from flask_login import login_user

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

    def login(self, email, password, follow=True):
        return self.client.post(
            url_for('auth.login'),
            data={'email': email, 'password': password},
            follow_redirects=follow
        )

    def logout(self, follow=True):
        return self.client.get(url_for('auth.logout'), follow_redirects=follow)

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

    def test_navbar_logged_out_user(self):
        resp = self.client.get(url_for('main.index'))
        self.assertIn(b'Login</a>', resp.data, 'Login link should appear')
        self.assertIn(b'Sign Up</a>', resp.data, 'Sign Up link should appear')

    def test_navbar_logged_in_user(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')
        self.login(user.email, 'pass')
        resp = self.client.get(url_for('main.index'))
        self.assertIn(b'Logout</a>', resp.data, 'Logout link should appear')
        self.assertNotIn(b'Login</a>', resp.data, 'Login link should not appear')


class TestAuth(BaseTest):

    def test_login_logout(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')
        resp = self.login(user.email, 'pass')
        self.assertIn(b'Login Successful', resp.data, 'Successful login message did not appear')
        resp = self.logout()
        self.assertIn(b'Logged out', resp.data, 'Logout message did not appear')

    def test_login_basic(self):
        resp = self.client.get(url_for('auth.login'))
        self.assert200(resp)
        self.assert_template_used('auth/login.html.j2')
        self.assertIn(b'<h1>Login</h1>', resp.data, 'Title missing')
        self.assertIn(b'>Reset Password</a>', resp.data, 'Reset password link missing')

    def test_login_no_user(self):
        resp = self.login('adam@example.com', 'pass')
        self.assert200(resp)
        self.assertIn(b'Invalid Email/Password', resp.data)

    def test_login_valid_user_invalid_pw(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        resp = self.login('adam@example.com', 'wrong')
        self.assert200(resp)
        self.assertIn(b'Invalid Email/Password', resp.data)

    def test_login_valid_user_valid_pw_no_follow(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        resp = self.login('adam@example.com', 'pass', False)
        self.assertRedirects(resp, url_for('main.index'), 'Should redirect to main.index')

    def test_login_unverified_message(self):
        acct = self.add_acct('Test Company')
        user = self.add_user(acct.id, 'Adam', 'Test', 'adam@example.com', 'pass')

        resp = self.login('adam@example.com', 'pass')
        self.assertIn(b'Your account is still not verified.', resp.data, 'Unverified message does not appear')
        self.logout()
        user.verified = True
        user.verified_date = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        resp = self.login('adam@example.com', 'pass')
        self.assertNotIn(b'Your account is still not verified.', resp.data, 'Unverified message does not appear')


if __name__ == '__main__':
    unittest.main()
