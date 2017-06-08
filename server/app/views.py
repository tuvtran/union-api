# server/app/views.py

from flask import (
    Blueprint,
    jsonify,
    request
)

from app.models import Company, Founder

companies_blueprint = Blueprint('companies', __name__)


@companies_blueprint.route('/companies', methods=['GET', 'POST'])
def companies():
    """GET to retrieve all the companies
    POST to create a new company
    """
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        company = Company(
            name=request.json['name'],
            bio=request.json['bio'],
            website=request.json['website'],
        )

        # TODO: add founders field

        company.save()
        data = {
            'id': company.id,
            'name': company.name,
            'bio': company.bio,
            'website': company.website,
            'founders': company.founders
        }
        return jsonify(data)


@companies_blueprint.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company:
        data = {
            'id': company.id,
            'name': company.name,
            'website': company.website,
            # TODO: figure out a way to add founders
            'founders': [],
            'bio': company.bio
        }
        return jsonify(data)
