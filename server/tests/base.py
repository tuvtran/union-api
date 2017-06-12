# server/tests/base.py

import json
from flask_testing import TestCase
from app import create_app, db


class BaseTestClass(TestCase):

    def send_POST(self, url, data):
        return self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )

    def get_id_from_POST(self, data):
        return json.loads(
            self.send_POST('/companies', data).data.decode()['id']
        )

    def create_app(self):
        return create_app(config_name='testing')

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
