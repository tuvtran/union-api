# server/tests/unit/auth/test_change_password.py

import json
from tests.base import BaseTestClass


class AuthChangePasswordTest(BaseTestClass):

    def test_change_password_not_logged_in(self):
        response = self.send_PUT('/auth/change', data={
            'email': 'tu@example.com',
            'old_password': '1234',
            'new_password': '5678'
        })
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_change_password_incorrect_old_password(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT('/auth/change', data={
            'new_email': 'staff@example.com',
            'old_password': 'testt',
            'new_password': 'testtt'
        }, headers=self.get_authorized_header(auth_token))
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('old password is incorrect', response_['message'])

    def test_change_password_successfully(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT('/auth/change', data={
            'new_email': 'staff@example.com',
            'old_password': 'test',
            'new_password': 'test123'
        }, headers=self.get_authorized_header(auth_token))
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn(
            'successfully changed login information', response_['message'])

    def test_change_email_successfully(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT('/auth/change', data={
            'new_email': 'staff_new@example.com',
            'old_password': 'test',
            'new_password': 'test123',
        }, headers=self.get_authorized_header(auth_token))
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn(
            'successfully changed login information', response_['message'])

    def test_login_after_change_password(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT('/auth/change', data={
            'new_email': 'staff@example.com',
            'old_password': 'test',
            'new_password': 'test123'
        }, headers=self.get_authorized_header(auth_token))
        response = self.send_POST('/auth/login', {
            'email': 'staff@example.com',
            'password': 'test123'
        })
        self.assert200(response)
