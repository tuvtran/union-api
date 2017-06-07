# server/tests/functional_test.py

from tests.base import BaseTestClass


class NewCompanyTest(BaseTestClass):

    def test_can_add_a_new_company(self):
        """Test user can send a POST request to the server"""
        # After months of waiting, finally Jane, Bookoo's founder,
        # received an acceptance letter from The Brandery, one of the
        # best startup incubators in the US. On her first day of arrival,
        # Jane heard about this cool shiny new KPI tracking API the interns
        # built. Excited, Jane tried sending a POST request with fake data.

        # After Jane sends a request, she receives a JSON object with a success
        # message and the content including her company's name, id in the
        # database,emails of the cofounders, bio and website.
        pass
