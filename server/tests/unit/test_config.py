# server/tests/test_config.py

from tests.base import BaseTestClass


class TestCurrentAppConfigurations(BaseTestClass):

    def test_app_is_testing(self):
        """Test current instance of app is running in testing mode
        and with test database
        """
        self.assertTrue(self.app.config['TESTING'])
        self.assertTrue(self.app.config['DEBUG'])
        self.assertEqual(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            'postgresql://localhost/test_db'
        )
        self.assertEqual(self.app.config['EXP'], 2)
