# server/tests/unit/kpi/test_get.py

import json
import datetime
from tests.base import BaseTestClass
from tests.sample_data import data1


class KpiGETTest(BaseTestClass):
    metrics = ['sales', 'customers', 'traffic', 'emails']

    # Format like "Fri, 16 Jun 2017 15:57:23 GMT"
    time_formatter = "%a, %d %b %Y %H:%M:%S GMT"

    def test_get_data_invalid_id(self):
        auth_token = self.get_auth_token(staff=True)
        response = self.client.get(
            '/companies/123/metrics',
            headers=self.get_authorized_header(auth_token))
        response_ = json.loads(response.data.decode())
        self.assert404(response)
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_get_data_when_there_is_no_data(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        response = self.client.get(
            f'/companies/{company_id}/metrics',
            headers=self.get_authorized_header(auth_token))
        self.assertEqual(response.status_code, 200)
        response_ = json.loads(response.data.decode())
        for metric in response_:
            self.assertEqual(response_[metric]['weeks'], 0)

    def test_get_data_one_week(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        self.send_POST(
            f'/companies/{company_id}',
            data=data,
            headers=self.get_authorized_header(auth_token)
        )

        response = self.client.get(
            f'/companies/{company_id}/metrics',
            headers=self.get_authorized_header(auth_token))
        response_ = json.loads(response.data.decode())

        self.assert200(response)

        for metric in response_:
            self.assertEqual(response_[metric]['weeks'], 1)
            self.assertIn('data', response_[metric])
            self.assertIn('last_updated', response_[metric])
            self.assertEqual(len(response_[metric]['data']), 1)
            self.assertEqual(response_[metric]['data'][0], data[metric])

            # The return object is valid if the last_updated field
            # is less than 2 minutes of the time making the request
            now = datetime.datetime.now()
            time_from_response = response_[metric]['last_updated']
            self.assertLess(
                now - datetime.datetime.strptime(
                    time_from_response, self.time_formatter),
                datetime.timedelta(days=0, minutes=2)
            )

    def test_get_data_many_weeks(self):
        auth_token = self.get_auth_token(staff=True)
        company_id = self.get_id_from_POST(data1)

        for i in range(4):
            self.send_POST(
                f'/companies/{company_id}',
                data=self.kpi_for_week(i),
                headers=self.get_authorized_header(auth_token)
            )

        response = self.client.get(
            f'/companies/{company_id}/metrics',
            headers=self.get_authorized_header(auth_token))
        response_ = json.loads(response.data.decode())

        self.assert200(response)

        for metric in response_:
            count = self.KPI[metric].query\
                .filter_by(company_id=company_id).count()
            self.assertEqual(response_[metric]['weeks'], count)
            self.assertIn('data', response_[metric])
            self.assertIn('last_updated', response_[metric])
            self.assertEqual(len(response_[metric]['data']), count)

            # The return object is valid if the last_updated field
            # is less than 2 minutes of the time making the request
            now = datetime.datetime.now()
            time_from_response = response_[metric]['last_updated']
            self.assertLess(
                now - datetime.datetime.strptime(
                    time_from_response, self.time_formatter),
                datetime.timedelta(days=0, minutes=2)
            )

            for i in range(count):
                weekly_kpis = self.kpi_for_week(i)
                self.assertEqual(response_[metric]['data'][i], weekly_kpis[metric])
