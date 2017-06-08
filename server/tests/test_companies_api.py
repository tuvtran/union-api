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

    def test_create_a_new_company_without_founders(self):
        """Test can send a POST request and create a new company."""
        response = self.client.post(
            '/companies',
            data=json.dumps(self.data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        company = Company.query.first()
        self.assertEqual(company.name, self.data['name'])
        self.assertEqual(company.website, self.data['website'])
        self.assertEqual(company.bio, self.data['bio'])

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
