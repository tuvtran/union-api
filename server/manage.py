# server/manage.py

import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app

app = create_app(config_name=os.environ.get('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables"""
    db.create_all()


@manager.command
def drop_db():
    """Drop all db tables"""
    db.drop_all()


@manager.command
def test(type):
    """Run the unit tests without code coverage."""
    try:
        tests = unittest.TestLoader().discover(
            f'tests/{type}',
            pattern='test*.py'
        )
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1
    except ImportError:
        print("There is no test like that!")


if __name__ == "__main__":
    manager.run()
