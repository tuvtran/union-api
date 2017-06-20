# server/tests/base.py

import json
from flask_testing import TestCase
from app import create_app, db
from app.models import (
    Founder,
    Sale,
    Customer,
    Traffic,
    Email
)
from tests.sample_data import kpis


class BaseTestClass(TestCase):
    KPI = {
        'sales': Sale,
        'customers': Customer,
        'traffic': Traffic,
        'emails': Email
    }

    def kpi_for_week(self, week=0):
        assert week < min(list(map(
            len, [
                kpis['sales'],
                kpis['customers'],
                kpis['traffic'],
                kpis['emails']
            ]
        )))
        return {
            'sales': kpis['sales'][week],
            'customers': kpis['customers'][week],
            'traffic': kpis['traffic'][week],
            'emails': kpis['emails'][week],
        }

    def get_authorized_header(self, token):
        return dict(Authorization=f'Bearer {token}')

    def get_auth_token(self, staff=False, company_id=None):
        if staff:
            auth = self.send_POST('auth/register', {
                'email': 'staff@example.com',
                'password': 'test',
                'staff': True
            })
        elif not staff and company_id:
            Founder(
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

    def send_PUT(self, url, data):
        return self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

    def GET_data(self, url):
        response = self.client.get(url)
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
