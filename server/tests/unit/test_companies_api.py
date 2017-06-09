# server/tests/test_companies.py

import json
from tests.base import BaseTestClass
from app.models import Company, Founder


class CompanyPOSTTest(BaseTestClass):

    def send_POST(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )

    def test_send_wrong_HTTP_requests(self):
        response1 = self.client.put(
            '/companies',
            data=''
        )
        self.assertEqual(response1.status_code, 405)

        response2 = self.client.delete(
            '/companies'
        )
        self.assertEqual(response2.status_code, 405)

    def test_send_empty_POST_request(self):
        response = self.send_POST('/companies', '')
        self.assertEqual(response.status_code, 400)

    def test_send_POST_request_without_name(self):
        response = self.send_POST('/companies', {
            'bio': 'Random bio'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_a_new_company_database(self):
        """>\tSee if data is in database"""
        response = self.send_POST('/companies', self.data)
        self.assertEqual(response.status_code, 201)
        company = Company.query.first()

        self.assertEqual(company.name, self.data['name'])
        self.assertEqual(company.website, self.data['website'])
        self.assertEqual(company.bio, self.data['bio'])
        self.assertRegex(str(list(company.founders)), '(.+)')
        self.assertIn('@demo.com', str(list(company.founders)))

    def test_can_retrieve_a_company_message(self):
        """>\tSee if returns the appropriate message"""
        response = self.send_POST('/companies', self.data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', data['status'])
        self.assertIn('new company created!', data['message'])
        self.assertIn('id', data)


class CompanyGETTest(BaseTestClass):

    def test_send_invalid_id(self):
        response = self.client.get('/companies/999999')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('failure', data['status'])
        self.assertIn('company not found', data['message'])

    def test_can_retrieve_a_company_without_founders(self):
        demo = Company(
            name=self.data['name'],
            website=self.data['website'],
            bio=self.data['bio'],
        )
        demo.save()
        company_id = Company.query.first().id

        # GET request
        response = self.client.get(f'/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        company = json.loads(response.data.decode())
        self.assertEqual(company['name'], self.data['name'])
        self.assertEqual(company['website'], self.data['website'])
        self.assertEqual(company['bio'], self.data['bio'])

    def test_can_retrieve_a_company_with_founders(self):
        demo = Company(
            name=self.data['name'],
            website=self.data['website'],
            bio=self.data['bio'],
        )
        demo.save()

        # Add founders into the database
        # with reference to the newly created company
        company_id = Company.query.first().id
        for founder in self.data['founders']:
            Founder(
                company_id=company_id,
                name=founder['name'],
                email=founder['email'],
                role=founder['role']
            ).save()

        # GET request
        response = self.client.get(f'/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        company = json.loads(response.data.decode())
        self.assertIn('founders', company)
        self.assertIn('role', str(company['founders']))
        self.assertIn('@demo.com', str(company['founders']))
