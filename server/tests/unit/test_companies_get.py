# server/tests/unit/test_companies_get.py

import json
from tests.base import BaseTestClass
from tests.sample_data import (
    data1,
    data2,
    data3
)
from app.models import Company, Founder


class CompanyGETTest(BaseTestClass):

    def test_send_invalid_id(self):
        response = self.client.get('/companies/999999')
        response_ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_can_retrieve_a_company_without_founders(self):
        demo = Company(
            name=data1['name'],
            website=data1['website'],
            bio=data1['bio'],
        )
        demo.save()
        company_id = Company.query.first().id

        # GET request
        response = self.client.get(f'/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        response_ = json.loads(response.data.decode())
        self.assertEqual(response_['name'], data1['name'])
        self.assertEqual(response_['website'], data1['website'])
        self.assertEqual(response_['bio'], data1['bio'])

    def test_can_retrieve_a_company_with_founders(self):
        demo = Company(
            name=data1['name'],
            website=data1['website'],
            bio=data1['bio'],
        )
        demo.save()

        # Add founders into the database
        # with reference to the newly created company
        company_id = Company.query.first().id
        for founder in data1['founders']:
            Founder(
                company_id=company_id,
                name=founder['name'],
                email=founder['email'],
                role=founder['role']
            ).save()

        # GET request
        response = self.client.get(f'/companies/{company_id}')
        self.assertEqual(response.status_code, 200)
        response_ = json.loads(response.data.decode())
        self.assertIn('founders', response_)
        self.assertIn('role', str(response_['founders']))
        self.assertIn('@demo.com', str(response_['founders']))

    def test_get_all_companies_0(self):
        """>\t With no company in database"""
        response = self.client.get('/companies')
        self.assertEqual(response.status_code, 200)
        response_ = json.loads(response.data.decode())
        self.assertEqual(response_['total'], 0)
        self.assertDictEqual(response_['companies'], {})

    def test_get_all_companies_3(self):
        """>\t With 3 companies in the database"""
        for data in [data1, data2, data3]:
            self.send_POST('/companies', data)

        response = self.client.get('/companies')
        response_ = json.loads(response.data.decode())

        self.assertIn('total', response_)
        self.assertIn('companies', response_)

        self.assertEqual(response_['total'], 3)

        companies = response_['companies']
        for name in companies:
            self.assertIn('id', companies[name])
            self.assertIn('bio', companies[name])
            self.assertIn('website', companies[name])
            self.assertIn('founders', companies[name])
            self.assertEqual(str(type(companies[name]['founders'])), "<class 'list'>")
            self.assertGreater(len(companies[name]['founders']), 0)

            for founder in companies[name]['founders']:
                self.assertIn('email', founder)
