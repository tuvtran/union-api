# server/tests/base.py

from flask_testing import TestCase
from app import create_app, db


class BaseTestClass(TestCase):
    data = {
        'name': 'Demo',
        'founders': [
            {
                'name': 'Tu Tran',
                'email': 'tu@demo.com',
                'role': 'CTO'
            },
            {
                'name': 'John Average',
                'email': 'john@demo.com',
                'role': 'CEO'
            }
        ],
        'website': 'http://www.demo.com',
        'bio': 'This is a demo company',
    }

    def create_app(self):
        return create_app(config_name='testing')

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
