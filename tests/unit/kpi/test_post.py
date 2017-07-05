# server/tests/unit/kpi/test_post.py

import json
import app.models
from tests.base import BaseTestClass
from tests.sample_data import data1, kpis


class KpiPOSTTest(BaseTestClass):

    def test_post_empty_metrics(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)

        response = self.send_POST(
            f'/companies/{company_id}',
            data='',
            headers=self.get_authorized_header(auth_token)
        )

        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn('empty metrics', response_['message'])

    def test_one_of_the_metrics_is_empty(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)

        # The assumption is that it's okay to add only 2 or 3
        # fields out of 4, but if there are 4 fields and there is
        # blank data for one of the fields then return an error
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': kpis['sales'][0],
                'subscribers': '',
                'traffic': kpis['traffic'][0],
                'preorders': kpis['preorders'][0],
            },
            headers=self.get_authorized_header(auth_token)
        )
        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'one of the metrics is empty',
            response_['message']
        )

    def test_post_to_invalid_company(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.send_POST(
            '/companies/1233', data=self.kpi_for_week(0),
            headers=self.get_authorized_header(auth_token))

        self.assert404(response)

        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_post_all_kpis_to_company_message(self):
        """>\tPOST all the KPIs successfully and returns the correct message"""
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        response = self.send_POST(
            f'/companies/{company_id}',
            data=data,
            headers=self.get_authorized_header(auth_token)
        )
        response_ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
        self.assertIn('metrics_added', response_)
        for metric in response_['metrics_added']:
            self.assertEqual(response_['metrics_added'][metric], data[metric])

    def test_post_one_kpi_to_company_message(self):
        """>\tPOST just one KPI successfully and returns the correct message"""
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': 123
            },
            headers=self.get_authorized_header(auth_token)
        )
        response_ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
        self.assertEqual(response_['metrics_added']['sales'], 123)

    def test_post_all_kpis_to_company_database(self):
        """>\tPOST all the KPIs successfully and adds data to the database"""
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        self.send_POST(
            f'/companies/{company_id}',
            data=data,
            headers=self.get_authorized_header(auth_token)
        )

        for metric in self.metrics:
            self.assertEqual(
                self.KPI[metric].query
                    .filter_by(company_id=company_id)[0].value,
                data[metric]
            )

    def test_post_one_kpi_to_company_database(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': 123
            },
            headers=self.get_authorized_header(auth_token)
        )
        sale = app.models.Sale.query.filter_by(company_id=company_id)
        traffic = app.models.Traffic.query.filter_by(
            company_id=company_id).first()
        self.assertEqual(sale[0].value, 123)
        self.assertIsNone(traffic)

    def test_post_all_kpis_to_company_many_weeks_database(self):
        """>\tPOST all the KPIs over the span of 4 weeks and
        check if the database has the information"""
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)

        for i in range(4):
            self.send_POST(
                f'/companies/{company_id}',
                data=self.kpi_for_week(i),
                headers=self.get_authorized_header(auth_token)
            )

        for i in range(4):
            weekly_kpis = self.kpi_for_week(i)

            for metric in self.metrics:
                metric_db = self.KPI[metric].query.filter_by(
                    company_id=company_id)

                # check for value
                self.assertEqual(metric_db[i].value, weekly_kpis[metric])

                # check for week number
                self.assertEqual(metric_db[i].week, i)
