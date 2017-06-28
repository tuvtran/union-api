# server/tests/unit/auth/test_register_status.py

import json
from tests.base import BaseTestClass


class AuthRegisterTest(BaseTestClass):

    def test_register_empty_request(self):
        response = self.send_POST('/auth/register', {})
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid register request', response_['message'])

    def test_register_lacking_field(self):
        response = self.send_POST('/auth/register', {
            'email': 'staff@brandery.org'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid register request', response_['message'])

    def test_register_email_exists(self):
        self.send_POST('/auth/register', {
            'email': 'tu@demo.com',
            'password': 'test123'
        })
        response = self.send_POST('/auth/register', {
            'email': 'tu@demo.com',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 202)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('user exists. log in instead', response_['message'])

    def test_register_successfully(self):
        response = self.send_POST('/auth/register', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assertEqual(response.status_code, 201)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('successfully registered', response_['message'])
        self.assertIn('auth_token', response_)


class AuthUserTest(BaseTestClass):

    def test_not_logged_in(self):
        response = self.client.get('auth/status')
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_logged_in(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.client.get(
            '/auth/status',
            headers=self.get_authorized_header(auth_token))
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('data', response_)
        self.assertIn('user_id', response_['data'])
        self.assertIn('email', response_['data'])
        self.assertIn('company', response_['data'])
        self.assertIn('registered_on', response_['data'])
        self.assertIn('staff', response_['data'])
