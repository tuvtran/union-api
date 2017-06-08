# server/tests/functional_test.py

import json
from tests.base import BaseTestClass


class NewCompanyTest(BaseTestClass):

    def test_can_add_a_new_company(self):
        """Test user can send a POST and GET request to the server"""
        # After months of waiting, finally Jane, Boocoo's founder,
        # received an acceptance letter from The Brandery, one of the
        # best startup incubators in the US. On her first day of arrival,
        # Jane heard about this cool shiny new KPI tracking API the interns
        # built. Excited, Jane tried sending a POST request with fake data.
        response = self.client.post(
            '/companies',
            data=json.dumps({
                'name': 'Boocoo',
                'founders': [
                    {'email': 'jane@boocoo.club'},
                    {'email': 'tu@boocoo.club'},
                    {'email': 'sed@boocoo.club'}
                ],
                'website': 'http://boocoo.club',
                'bio': """
                    Boocoo is a AI startup specializing in random stuff
                """
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)

        # After Jane sends a request, she receives a JSON object with a success
        # message and her company's id in the databse
        data = json.loads(response.data.decode())
        self.assertIn('id', data)
        self.assertIn('success', data['status'])
        self.assertIn('new company created!', data['message'])

        # Once she gets the id, she tries calling the server to fetch the
        # company's data.
        boocoo_id = data['id']
        get_response = self.client.get(f'/companies/{boocoo_id}')
        self.assertEqual(get_response, 200)
        self.assertIn('id', str(get_response.data))
        self.assertIn('name', str(get_response.data))
        self.assertIn('founders', str(get_response.data))

        # Tada! It works! Now she can be sure that she could both send
        # a POST request to create her new company and fetch that using
        # a GET request
