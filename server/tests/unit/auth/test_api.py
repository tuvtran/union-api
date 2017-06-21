# server/tests/unit/auth/test_login.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1, data2


class AuthCompanyApiTest(BaseTestClass):

    def test_non_staff_not_allowed_to_get_all_companies(self):
        company_id = self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=company_id)
        response = self.client.get(
            '/companies', headers=self.get_authorized_header(auth_token))
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('non-staff members not allowed', response_['message'])

    def test_not_logged_in_get_all_companies(self):
        response = self.client.get(
            '/companies')
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_non_staff_not_allowed_to_create_company(self):
        self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=1)
        response = self.send_POST(
            '/companies', data=data2,
            headers=self.get_authorized_header(auth_token))
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('non-staff members not allowed', response_['message'])

    def test_not_logged_in_create_company(self):
        response = self.send_POST(
            '/companies', data=data2)
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('unauthorized', response_['message'])

    def test_different_employee_get_a_company(self):
        company_id1 = self.get_id_from_POST(data1)
        auth_token1 = self.get_auth_token(staff=False, company_id=company_id1)
        company_id2 = self.get_id_from_POST(data2)
        response = self.client.get(
            f'/companies/{company_id2}',
            headers=self.get_authorized_header(auth_token1)
        )
        self.assert401(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('user not authorized to this view', response_['message'])

    def test_respective_employee_allowed_to_one_company(self):
        company_id = self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=False, company_id=company_id)
        response = self.client.get(
            f'/companies/{company_id}',
            headers=self.get_authorized_header(auth_token)
        )
        self.assert200(response)


class AuthKpiApiTest(BaseTestClass):
    pass
