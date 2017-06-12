# server/app/apis/__init__.py

from flask import Blueprint

companies_blueprint = Blueprint('companies', __name__)
kpi_blueprint = Blueprint('kpi', __name__)

from app.apis import companies, kpi      # noqa
