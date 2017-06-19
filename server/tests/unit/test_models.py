# server/tests/unit/test_models.py

from app import db
from app.models import (
    Company,
    Sale,
    # User
)
from tests.base import BaseTestClass
from tests.sample_data import data1, kpis


class MetricTest(BaseTestClass):

    def test_get_latest_added_date(self):
        company_id = self.get_id_from_POST(data1)
        for metric in self.KPI:
            for data in kpis[metric]:
                self.KPI[metric](
                    company_id=company_id,
                    value=data,
                ).save()

        # Check if the last data added to the database is
        # the one that the last_updated method returns correctly
        for metric in self.KPI:
            metric_class = self.KPI[metric]
            self.assertEqual(
                metric_class.get_last_updated(company_id),
                metric_class.query.all()[-1]
            )

    def test_date_is_updated_when_data_changes(self):
        company_id = self.get_id_from_POST(data1)

        for metric in self.KPI:
            for data in kpis[metric]:
                self.KPI[metric](
                    company_id=company_id,
                    value=data,
                ).save()

        updated_time = Sale.get_last_updated(company_id).updated_at

        Sale.get_last_updated(company_id).value = 234
        db.session.commit()
        new_updated_time = Sale.get_last_updated(company_id).updated_at

        self.assertNotEqual(updated_time, new_updated_time)


class UserTest(BaseTestClass):

    def test_encode_auth_token(self):
        user = User(
            email="tu@brandery.org",
            password="test"
        )
        user.save()
        auth_token = user.encode_auth_token(user.id)
        self.asserTrue(isinstance(auth_token, bytes))

    # def test_save_founder_automatically_save_user(self):
    #     Company()
