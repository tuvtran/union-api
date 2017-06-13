# server/tests/unit/test_kpi_api.py

import json
from app.models import Sale, Customer, Traffic, Email
from tests.base import BaseTestClass
from tests.sample_data import data1, kpis

KPI = {
    'sales': Sale,
    'customers': Customer,
    'traffic': Traffic,
    'emails': Email
}


class KpiPOSTTest(BaseTestClass):

    def test_post_empty_metrics(self):
        company_id = self.get_id_from_POST(data1)

        response = self.send_POST(
            f'/companies/{company_id}',
            data=''
        )

        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn('empty metrics', response_['message'])

    def test_one_of_the_metrics_is_empty(self):
        company_id = self.get_id_from_POST(data1)

        # The assumption is that it's okay to add only 2 or 3
        # fields out of 4, but if there are 4 fields and there is
        # blank data for one of the fields then return an error
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': kpis['sales'][0],
                'customers': '',
                'traffic': kpis['traffic'][0],
                'emails': kpis['emails'][0],
            }
        )
        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'one of the metrics is empty',
            response_['message']
        )

    def test_post_to_invalid_company(self):
        response = self.send_POST('/companies/1233', data=self.kpi_for_week(0))

        self.assert404(response)

        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_post_all_kpis_to_company_message(self):
        """>\tPOST all the KPIs successfully and returns the correct message"""
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        response = self.send_POST(
            f'/companies/{company_id}',
            data=data
        )
        response_ = json.loads(response.data.decode())
        self.assert200(response)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
        self.assertIn('metrics_added', response_)
        for metric in response_['metrics_added']:
            self.assertEqual(response_['metrics_added'][metric], data[metric])

    def test_post_one_kpi_to_company_message(self):
        """>\tPOST just one KPI successfully and returns the correct message"""
        company_id = self.get_id_from_POST(data1)
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': 123
            }
        )
        response_ = json.loads(response.data.decode())
        self.assert200(response)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
        self.assertEqual(response_['metrics_added']['sales'], 123)

    def test_post_all_kpis_to_company_database(self):
        """>\tPOST all the KPIs successfully and adds data to the database"""
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        self.send_POST(
            f'/companies/{company_id}',
            data=data
        )
        sale = Sale.query.filter_by(company_id=company_id)
        customers = Customer.query.filter_by(company_id=company_id)
        traffic = Traffic.query.filter_by(company_id=company_id)
        emails = Email.query.filter_by(company_id=company_id)
        self.assertEqual(sale[0].value, data['sales'])
        self.assertEqual(customers[0].value, data['customers'])
        self.assertEqual(traffic[0].value, data['traffic'])
        self.assertEqual(emails[0].value, data['emails'])

    def test_post_one_kpi_to_company_database(self):
        company_id = self.get_id_from_POST(data1)
        self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': 123
            }
        )
        sale = Sale.query.filter_by(company_id=company_id)
        customers = Customer.query.filter_by(company_id=company_id).first()
        traffic = Traffic.query.filter_by(company_id=company_id).first()
        emails = Email.query.filter_by(company_id=company_id).first()
        self.assertEqual(sale[0].value, 123)
        self.assertIsNone(customers)
        self.assertIsNone(traffic)
        self.assertIsNone(emails)

    def test_post_all_kpis_to_company_many_weeks_database(self):
        """>\tPOST all the KPIs over the span of 4 weeks and
        check if the database has the information"""
        company_id = self.get_id_from_POST(data1)

        for i in range(4):
            self.send_POST(
                f'/companies/{company_id}',
                data=self.kpi_for_week(i)
            )

        sale = Sale.query.filter_by(company_id=company_id)
        customers = Customer.query.filter_by(company_id=company_id)
        traffic = Traffic.query.filter_by(company_id=company_id)
        emails = Email.query.filter_by(company_id=company_id)

        for i in range(4):
            weekly_kpis = self.kpi_for_week(i)
            # Check for value
            self.assertEqual(sale[i].value, weekly_kpis['sales'])
            self.assertEqual(customers[i].value, weekly_kpis['customers'])
            self.assertEqual(traffic[i].value, weekly_kpis['traffic'])
            self.assertEqual(emails[i].value, weekly_kpis['emails'])

            # Check for week number
            self.assertEqual(sale[i].week, i)
            self.assertEqual(customers[i].week, i)
            self.assertEqual(traffic[i].week, i)
            self.assertEqual(emails[i].week, i)


class KpiGETTest(BaseTestClass):
    metrics = ['sales', 'customers', 'traffic', 'emails']

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
