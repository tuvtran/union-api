# server/tests/unit/companies.py

import json
import unittest
from tests.base import BaseTestClass
from tests.sample_data import data1


@unittest.skip
class CompanyPUTTest(BaseTestClass):

    def test_update_to_invalid_company(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT('/companies/123', {
            'name': 'Different',
            'website': 'https://different.com',
            'bio': 'This bio is different now'
        }, headers=self.get_authorized_header(auth_token))
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_update_to_valid_company(self):
        company_id = self.get_id_from_POST(data1)
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT(f'/companies/{company_id}', {
            'name': 'Different',
            'website': 'https://different.com',
            'bio': 'This bio is different now'
        }, headers=self.get_authorized_header(auth_token))
        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('info updated', response_['message'])
