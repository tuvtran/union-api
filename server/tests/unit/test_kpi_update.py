# server/tests/unit/test_kpi_update.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1


class KpiUpdateTest(BaseTestClass):

    def test_update_when_there_is_one_data(self):
        company_id = self.get_id_from_POST(data1)
        self.send_POST(f'/companies/{company_id}', data=self.kpi_for_week())

        # first_data = self.GET_data(f'/companies/{company_id}/sales')

        response = self.send_PUT(
            f'/companies/{company_id}/update',
            self.kpi_for_week(1)
        )

        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('resource updated', response_['message'])

        second_data = self.GET_data(f'/companies/{company_id}/sales')

        # self.assertNotEqual(
        #     first_data['last_updated'],
        #     second_data['last_updated']
        # )

        self.assertEqual(
            second_data['data'][0],
            self.kpi_for_week(1)['sales']
        )

    def test_update_when_there_is_no_data(self):
        company_id = self.get_id_from_POST(data1)
        response = self.send_PUT(
            f'/companies/{company_id}/update',
            self.kpi_for_week()
        )

        self.assert400(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('there is no data to update', response_['message'])

    def test_update_to_invalid_id(self):
        response = self.send_PUT('/companies/123/update', self.kpi_for_week())
        self.assert404(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_update_to_existing_data(self):
        company_id = self.get_id_from_POST(data1)
        self.send_POST(f'/companies/{company_id}', self.kpi_for_week(0))
        self.send_POST(f'/companies/{company_id}', self.kpi_for_week(1))
        response = self.send_PUT(
            f'/companies/{company_id}/update',
            self.kpi_for_week(2)
        )

        self.assert200(response)
        response_ = json.loads(response.data.decode())
        self.assertIn('success', response_['status'])
        self.assertIn('resource updated', response_['message'])

        updated_data = self.GET_data(f'/companies/{company_id}/sales')

        self.assertEqual(
            updated_data['data'][~0],
            self.kpi_for_week(2)['sales']
        )
