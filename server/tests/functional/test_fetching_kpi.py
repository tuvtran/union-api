# server/tests/functional/test_fetching_kpi.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1, kpis


class KPITest(BaseTestClass):

    def test_create_a_company_and_add_kpi_metrics(self):
        # Jane adds her startup to the database by sending
        # a POST request and get the company's id
        company_id = self.get_id_from_POST(data1)

        # Getting the company unique id in the database, she
        # adds the KPI tracking information for the first week.
        kpi_response = json.loads(self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': kpis['sales'][0],
                'customers': kpis['customers'][0],
                'traffic': kpis['traffic'][0],
                'emails': kpis['emails'][0],
            }
        ).data.decode())

        # She sees that in the returned message, there
        # are company name, message, status, and metrics added
        self.assertIn('success', kpi_response['status'])
        self.assertIn('metrics added', kpi_response['message'])
        self.assertIn('metrics_added', kpi_response)

        kpi = kpi_response['metrics_added']

        self.assertIn('sales', kpi)
        self.assertIn('customers', kpi)
        self.assertIn('traffic', kpi)
        self.assertIn('emails', kpi)

        # She checks if the returned metrics are the same as
        # what she inputs in earlier
        sales = kpi['sales']
        customers = kpi['customers']
        traffic = kpi['traffic']
        emails = kpi['emails']

        self.assertEqual(sales, kpis['sales'][0])
        self.assertEqual(customers, kpis['customers'][0])
        self.assertEqual(traffic, kpis['traffic'][0])
        self.assertEqual(emails, kpis['emails'][0])

        # Ensured they are equal, she now sends a GET request
        # as a last step to make sure
        get_sales = json.loads(
            self.client.get(f'/companies/{company_id}/sales').data.decode()
        )
        get_customers = json.loads(
            self.client.get(f'/companies/{company_id}/customers').data.decode()
        )
        get_traffic = json.loads(
            self.client.get(f'/companies/{company_id}/traffic').data.decode()
        )
        get_emails = json.loads(
            self.client.get(f'/companies/{company_id}/emails').data.decode()
        )

        # And check if the fields are all equal
        self.assertEqual(get_sales['data'][~0], sales)
        self.assertEqual(get_customers['data'][~0], customers)
        self.assertEqual(get_traffic['data'][~0], traffic)
        self.assertEqual(get_emails['data'][~0], emails)
