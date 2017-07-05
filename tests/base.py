# server/tests/base.py

import json
import app.models
from flask_testing import TestCase
from app import create_app, db
from tests.sample_data import kpis


class BaseTestClass(TestCase):
    KPI = {
        'sales': app.models.Sale,
        'traffic': app.models.Traffic,
        'subscribers': app.models.Subscriber,
        'engagement': app.models.Engagement,
        'mrr': app.models.MRR,
        'pilots': app.models.Pilot,
        'active_users': app.models.ActiveUser,
        'paying_users': app.models.PayingUser,
        'cpa': app.models.CPA,
        'product_releases': app.models.ProductRelease,
        'preorders': app.models.Preorder,
        'automation_percents': app.models.AutomationPercentage,
        'conversion_rate': app.models.ConversionRate,
        'marketing_spent': app.models.MarketingSpent,
        'other_1': app.models.Other1,
        'other_2': app.models.Other2,
    }

    metrics = [
        'sales', 'traffic', 'subscribers',
        'active_users', 'paying_users', 'engagement',
        'mrr', 'cpa', 'pilots', 'product_releases', 'preorders',
        'automation_percents', 'conversion_rate', 'marketing_spent',
        'other_1', 'other_2']

    def kpi_for_week(self, week=0):
        assert week < min(list(map(
            len, [kpis[metric] for metric in kpis]
        )))
        return_obj = {}
        for metric in kpis:
            return_obj[metric] = kpis[metric][week]

        return return_obj

    def get_authorized_header(self, token):
        return dict(Authorization=f'Bearer {token}')

    def get_auth_token(self, staff=False, company_id=None):
        if staff:
            app.models.User(
                name="Staff",
                email="staff@example.com",
                password="test",
                staff=True
            ).save()
            auth = self.send_POST('auth/login', {
                'email': 'staff@example.com',
                'password': 'test',
            })
        elif not staff and company_id:
            app.models.Founder(
                name="Tu",
                email="tu@example.com",
                role="CEO",
                company_id=company_id
            ).save()
            auth = self.send_POST('auth/login', {
                'email': 'tu@example.com',
                'password': 'founder',
                'staff': False
            })
        return json.loads(auth.data.decode())['auth_token']

    def send_POST(self, url, data, headers=None):
        return self.client.post(
            url,
            data=json.dumps(data),
            headers=headers,
            content_type="application/json"
        )

    def send_PUT(self, url, data, headers=None):
        return self.client.put(
            url,
            data=json.dumps(data),
            headers=headers,
            content_type='application/json',
        )

    def GET_data(self, url, headers=None):
        response = self.client.get(url, headers=headers)
        return json.loads(response.data.decode())

    def get_id_from_POST(self, data):
        # Because we are creating a new company, we need
        # to log in as staff
        auth_token = self.get_auth_token(staff=True)
        return json.loads(
            self.send_POST(
                '/companies',
                data=data,
                headers=self.get_authorized_header(auth_token)
            ).data.decode()
        )['id']

    def create_app(self):
        return create_app(config_name='testing')

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
