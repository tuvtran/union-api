# server/tests/unit/test_kpi_get.py

import json
from app.models import Sale, Customer, Traffic, Email
from tests.base import BaseTestClass
from tests.sample_data import data1

KPI = {
    'sales': Sale,
    'customers': Customer,
    'traffic': Traffic,
    'emails': Email
}


class KpiGETTest(BaseTestClass):
    metrics = ['sales', 'customers', 'traffic', 'emails']

    def test_invalid_metric_api_call(self):
        company_id = self.get_id_from_POST(data1)
        response = self.client.get(f'/companies/{company_id}/nonexistent')
        self.assert404(response)

    def test_get_data_invalid_id(self):
        response = self.client.get('/companies/123/sales')
        response_ = json.loads(response.data.decode())
        self.assert404(response)
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_get_data_one_week(self):
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        self.send_POST(
            f'/companies/{company_id}',
            data=data
        )

        for metric in self.metrics:
            response = self.client.get(f'/companies/{company_id}/{metric}')
            response_ = json.loads(response.data.decode())

            self.assert200(response)
            self.assertEqual(response_['weeks'], 1)
            self.assertIn('data', response_)
            self.assertEqual(len(response_['data']), 1)
            self.assertEqual(response_['data'][0], data[metric])

    def test_get_data_many_weeks(self):
        company_id = self.get_id_from_POST(data1)

        for i in range(4):
            self.send_POST(
                f'/companies/{company_id}',
                data=self.kpi_for_week(i)
            )

        for metric in self.metrics:
            count = KPI[metric].query.filter_by(company_id=company_id).count()

            response = self.client.get(f'/companies/{company_id}/{metric}')
            response_ = json.loads(response.data.decode())

            self.assert200(response)
            self.assertEqual(response_['weeks'], count)
            self.assertIn('data', response_)
            self.assertEqual(len(response_['data']), count)

            for i in range(count):
                weekly_kpis = self.kpi_for_week(i)
                self.assertEqual(response_['data'][i], weekly_kpis[metric])
