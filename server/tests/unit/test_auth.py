# server/tests/unit/test_auth.py

import json
from app.models import User
from tests.base import BaseTestClass
from tests.sample_data import data1


class AuthLoginTest(BaseTestClass):

    def test_login_user_does_not_exist(self):
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'wrong password or user does not exist', response_['message'])

    def test_login_invalid_email(self):
        response = self.send_POST('/auth/login', {
            'email': '',
            'password': 'staff'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_login_no_password(self):
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org'
        })
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_empty_request(self):
        response = self.send_POST('/auth/login', {})
        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('invalid login request', response_['message'])

    def test_login_staff_member(self):
        User(
            name="Staff",
            email="staff@brandery.org",
            password="staff",
        ).save()
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('auth_token', response_)
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged in', response_['message'])

    def test_login_founder(self):
        self.get_id_from_POST(data1)
        response = self.send_POST('/auth/login', {
            'email': 'john@demo.com',
            'password': 'founder'
        })
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('auth_token', response_)
        self.assertIn('success', response_['status'])
        self.assertIn('successfully logged in', response_['message'])

    def test_login_wrong_password(self):
        User(
            name="Staff",
            email="staff@brandery.org",
            password="staff",
        ).save()
        response = self.send_POST('/auth/login', {
            'email': 'staff@brandery.org',
            'password': 'staffff'
        })
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'wrong password or user does not exist', response_['message'])


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
        response = self.send_POST('auth/register', {
            'email': 'staff@brandery.org',
            'password': 'staff'
        })
        self.assertEqual(response.status_code, 201)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('successfully registered', response_['message'])
        self.assertIn('auth_token', response_)


class AuthUserTest(BaseTestClass):

    def test_view_user_status(self):
        pass
