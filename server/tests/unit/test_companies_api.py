# server/tests/test_companies.py

import json
from tests.base import BaseTestClass
from app.models import Company, Founder


class CompanyApiTest(BaseTestClass):
    data = {
        'name': 'Demo',
        'founders': [
            {'email': 'tu@demo.com'},
            {'email': 'john@demo.com'}
        ],
        'website': 'http://www.demo.com',
        'bio': 'This is a demo company',
    }

    def send_POST(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )

    def test_send_empty_POST_request(self):
        """Test sending empty POST request
        results in 400 status code
        """
        response = self.send_POST('/companies', '')
        self.assertEqual(response.status_code, 400)

    def test_send_POST_request_without_name(self):
        """Test sending POST request without name results
        in 400 status code
        """
        response = self.send_POST('/companies', {
            'bio': 'Random bio'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_a_new_company_database(self):
        """Test can send a POST request and create a new company.
        Test if data has been saved to the database
        """
        response = self.send_POST('/companies', self.data)
        self.assertEqual(response.status_code, 201)
        company = Company.query.first()

        self.assertEqual(company.name, self.data['name'])
        self.assertEqual(company.website, self.data['website'])
        self.assertEqual(company.bio, self.data['bio'])
        self.assertIn('@demo.com', list(company.founders))

    def test_can_retrieve_a_company_message(self):
        """Test can send a POST request and create a new company.
        Check the message and status code
        """
        response = self.send_POST('/companies', self.data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', data['status'])
        self.assertIn('new company created!', data['message'])
        self.assertIn('id', data)

    def test_can_retrieve_a_company_without_founders(self):
        """Test can send a GET request to retrieve company's info
        based on ID"""
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
        """Test can send a GET request to retrieve company's info
        based on ID with founders"""
        # Add a new company to the database
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
            Founder(company_id=company_id, email=founder['email']).save()

        # GET request
        response = self.client.get(f'/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        company = json.loads(response.data.decode())
        self.assertIn('founders', company)
        self.assertIn('@demo.com', company['founders'])
