# server/tests/test_companies.py

import json
from tests.base import BaseTestClass
from tests.sample_data import (
    data1,
    data2,
    data3
)
from app.models import Company, Founder


class CompanyPOSTTest(BaseTestClass):

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
        response = self.send_POST('/companies', data1)
        self.assertEqual(response.status_code, 201)
        company = Company.query.first()

        self.assertEqual(company.name, data1['name'])
        self.assertEqual(company.website, data1['website'])
        self.assertEqual(company.bio, data1['bio'])
        self.assertRegex(str(list(company.founders)), '(.+)')
        self.assertIn('@demo.com', str(list(company.founders)))

    def test_can_create_a_company_message(self):
        """>\tSee if returns the appropriate message"""
        response = self.send_POST('/companies', data1)
        response_ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response_['status'])
        self.assertIn('new company created!', response_['message'])
        self.assertIn('id', response_)

    def test_cannot_add_duplicate_companies(self):
        self.send_POST('/companies', data1)
        response = self.send_POST('/companies', data1)

        self.assertEqual(response.status_code, 400)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'company already exists',
            response_['message']
        )


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
        self.assertEqual(len(response_['companies']), 0)

    def test_get_all_companies_3(self):
        """>\t With 3 companies in the database"""
        for data in [data1, data2, data3]:
            self.send_POST('/companies', data)

        response = self.client.get('/companies')
        response_ = json.loads(response.data.decode())

        self.assertIn('total', response_)
        self.assertIn('companies', response_)

        self.assertEqual(response_['total'], 3)
        self.assertEqual(len(response_['companies']), 3)

        for company in response_['companies']:
            self.assertIn('id', company)
            self.assertIn('name', company)
            self.assertIn('bio', company)
            self.assertIn('website', company)
            self.assertIn('founders', company)
            self.assertEqual(str(type(company['founders'])), "<class 'list'>")
            self.assertGreater(len(company['founders']), 0)

            for founder in company['founders']:
                self.assertIn('email', founder)
