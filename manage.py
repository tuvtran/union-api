# manage.py

import os
import random
import coverage
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from populate import companies, KPI
from app import db, create_app
from app.models import (
    Company,
    Founder,
    User,
)

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        '**/__init__.py',
        'venv/*',
        '/usr/local/*',
    ]
)
COV.start()

app = create_app(config_name=os.environ.get('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

is_production = (os.environ.get('APP_SETTINGS') == 'production')


@manager.command
def createdb():
    """Creates the db tables"""
    db.create_all()
    db.session.commit()


@manager.command
def dropdb():
    """Drop all db tables"""
    db.drop_all()


@manager.command
def resetdb():
    """Reset all db tables"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def populate():
    """Populate some data"""
    db.drop_all()
    db.create_all()
    staff = User(
        name="Staff",
        password="test",
        email="staff@brandery.org",
        staff=True)

    staff.save()

    for company in companies:
        new_company = Company(
            name=company['name'],
            website=company['website'],
            bio=company['bio']
        )

        print('Saving company', new_company)

        new_company.save()

        if is_production:
            # We only add dummy data points
            # if not in production mode
            # Saving random metrics
            for _ in range(10):
                for metric in KPI:
                    KPI[metric](
                        company_id=new_company.id, value=random.randint(0, 100)
                    ).save()

        for founder in company['founders']:
            new_founder = Founder(
                name=founder['name'],
                email=founder['email'],
                role=founder['role'],
                company_id=new_company.id
            )

            print('Saving founder', founder)

            new_founder.save()

    db.session.commit()


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests/unit')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def test(type=""):
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
