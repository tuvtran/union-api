# server/app/views.py

from flask import (
    Blueprint,
    jsonify,
    request,
    make_response,
    abort
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
        # If data is empty or there is no field
        if not (request.json and 'name' in request.json):
            abort(400)

        company = Company(
            name=request.json['name'],
            bio=request.json['bio'],
            website=request.json['website'],
        )
        company.save()

        # if user sends founder list
        if 'founders' in request.json:
            for founder in request.json['founders']:
                Founder(
                    email=founder.get('email', ''),
                    name=founder.get('name', ''),
                    role=founder.get('role', '')
                ).save()

        data = {
            'status': 'success',
            'message': 'new company created!',
            'id': company.id
        }
        return make_response(jsonify(data)), 201


@companies_blueprint.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get(company_id)
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
