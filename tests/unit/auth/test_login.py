# server/tests/unit/auth/test_login.py

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
        self.assertIn('registered_on', response_)
        self.assertIn('company', response_)
        self.assertIn('company_id', response_)
        self.assertIn('staff', response_)
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
