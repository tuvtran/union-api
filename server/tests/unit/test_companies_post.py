# server/tests/test_companies_post.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1
from app.models import Company, Founder


class CompanyPOSTTest(BaseTestClass):

    def test_send_wrong_HTTP_requests(self):
        auth_token = self.get_auth_token(staff=True)
        response1 = self.client.put(
            '/companies',
            data='',
            headers=self.get_authorized_header(auth_token)
        )
        self.assertEqual(response1.status_code, 405)

        response2 = self.client.delete(
            '/companies',
            headers=self.get_authorized_header(auth_token)
        )
        self.assertEqual(response2.status_code, 405)

    def test_send_empty_POST_request(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_POST(
            '/companies', '', headers=self.get_authorized_header(auth_token))
        self.assertEqual(response.status_code, 400)

    def test_send_POST_request_without_name(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_POST('/companies', {
            'bio': 'Random bio',
        }, headers=self.get_authorized_header(auth_token))
        self.assertEqual(response.status_code, 400)

    def test_create_a_new_company_database(self):
        """>\tSee if data is in database"""
        auth_token = self.get_auth_token(staff=True)
        response = self.send_POST(
            '/companies', data1,
            headers=self.get_authorized_header(auth_token))
        self.assertEqual(response.status_code, 201)
        company = Company.query.first()

        self.assertEqual(company.name, data1['name'])
        self.assertEqual(company.website, data1['website'])
        self.assertEqual(company.bio, data1['bio'])
        self.assertRegex(str(list(company.founders)), '(.+)')
        self.assertIn('@demo.com', str(list(company.founders)))

    def test_create_a_new_company_with_founders(self):
        company_id = self.get_id_from_POST(data1)
        founders = Founder.query.filter_by(company_id=company_id)
        for index, founder in enumerate(founders):
            self.assertEqual(founder.name, data1['founders'][index]['name'])
            self.assertEqual(founder.email, data1['founders'][index]['email'])
            self.assertEqual(founder.role, data1['founders'][index]['role'])

    def test_can_create_a_company_message(self):
        """>\tSee if returns the appropriate message"""
        auth_token = self.get_auth_token(staff=True)
        response = self.send_POST(
            '/companies', data1,
            headers=self.get_authorized_header(auth_token))
        response_ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response_['status'])
        self.assertIn('new company created!', response_['message'])
        self.assertIn('id', response_)

    def test_cannot_add_duplicate_companies(self):
        auth_token = self.get_auth_token(staff=True)
        self.send_POST(
            '/companies', data1,
            headers=self.get_authorized_header(auth_token))
        response = self.send_POST(
            '/companies', data1,
            headers=self.get_authorized_header(auth_token))

        self.assertEqual(response.status_code, 400)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'company already exists',
            response_['message']
        )

        # Check that the database does not add the second company
        self.assertEqual(Company.query.count(), 1)
