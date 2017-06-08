# server/tests/base.py

from flask_testing import TestCase
from app import create_app, db


class BaseTestClass(TestCase):
    data = {
        'name': 'Demo',
        'founders': [
            {'email': 'tu@demo.com'},
            {'email': 'john@demo.com'}
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
