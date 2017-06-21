# server/tests/unit/kpi/test_update.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1


class KpiUpdateTest(BaseTestClass):

    def test_update_when_there_is_one_data(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        self.send_POST(
            f'/companies/{company_id}', data=self.kpi_for_week(),
            headers=self.get_authorized_header(auth_token))

        response = self.send_PUT(
            f'/companies/{company_id}/metrics',
            self.kpi_for_week(1),
            headers=self.get_authorized_header(auth_token)
        )

        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('resource updated', response_['message'])

        second_data = self.GET_data(
            f'/companies/{company_id}/metrics',
            headers=self.get_authorized_header(auth_token))

        for metric in second_data:
            self.assertEqual(
                self.kpi_for_week(1)[metric],
                second_data[metric]['data'][0]
            )

    def test_update_when_there_is_no_data(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        response = self.send_PUT(
            f'/companies/{company_id}/metrics',
            self.kpi_for_week(),
            headers=self.get_authorized_header(auth_token)
        )

        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('there is no data to update', response_['message'])

    def test_update_to_invalid_id(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_PUT(
            '/companies/123/metrics', self.kpi_for_week(),
            headers=self.get_authorized_header(auth_token))
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_update_to_existing_data(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        self.send_POST(
            f'/companies/{company_id}', self.kpi_for_week(0),
            headers=self.get_authorized_header(auth_token))
        self.send_POST(
            f'/companies/{company_id}', self.kpi_for_week(1),
            headers=self.get_authorized_header(auth_token))
        response = self.send_PUT(
            f'/companies/{company_id}/metrics',
            self.kpi_for_week(2),
            headers=self.get_authorized_header(auth_token)
        )

        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('resource updated', response_['message'])

        updated_data = self.GET_data(
            f'/companies/{company_id}/metrics',
            headers=self.get_authorized_header(auth_token))

        for metric in updated_data:
            self.assertEqual(
                self.kpi_for_week(2)[metric],
                updated_data[metric]['data'][~0]
            )
