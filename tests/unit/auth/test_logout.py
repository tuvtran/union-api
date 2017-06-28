# server/tests/unit/auth/test_logout.py

import json
import time
import unittest
from tests.base import BaseTestClass


class AuthLogoutTest(BaseTestClass):

    @unittest.skip
    def test_valid_logout(self):
        auth_token = self.get_auth_token(staff=True)
        # user log out
        response = self.send_POST(
            '/auth/logout',
            data=None,
            headers=self.get_authorized_header(auth_token)
        )
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged out', response_['message'])

        status_response = self.client.get(
            '/auth/status', headers=self.get_authorized_header(auth_token))
        self.assert401(status_response)
        status_response_ = json.loads(status_response.data.decode())
        self.assertIn('failure', status_response_['status'])

    def test_never_logged_in(self):
        response = self.send_POST(
            '/auth/logout',
            data=None,
        )
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_expired_token(self):
        auth_token = self.get_auth_token(staff=True)
        time.sleep(3)
        response = self.send_POST(
            '/auth/logout',
            data=None,
            headers=self.get_authorized_header(auth_token)
        )
        response_ = json.loads(response.data.decode())
        self.assert500(response)
        self.assertIn('failure', response_['status'])
