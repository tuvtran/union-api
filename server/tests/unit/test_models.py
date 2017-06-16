# server/tests/unit/test_models.py

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
                metric_class.last_updated(company_id),
                metric_class.query.all()[-1]
            )


class UserTest(BaseTestClass):
    pass
