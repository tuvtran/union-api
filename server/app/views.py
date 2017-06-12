# server/app/views.py

from flask import (
    Blueprint,
    jsonify,
    request,
    make_response,
    abort
)
from sqlalchemy.exc import IntegrityError

from app.models import (
    Company,
    Founder,
    Sale,
    Customer,
    Traffic,
    Email
)

companies_blueprint = Blueprint('companies', __name__)

KPI = {
    'sales': Sale,
    'customers': Customer,
    'traffic': Traffic,
    'emails': Email
}


def get_all_companies():
    companies = list(map(
        lambda company: {
            'id': company.id,
            'name': company.name,
            'website': company.website,
            'bio': company.bio,
            'founders': list(map(
                lambda founder: {
                    'name': founder.name,
                    'email': founder.email,
                    'role': founder.role
                },
                company.founders
            )),
        },
        Company.query.all()
    ))

    return jsonify({
        'total': Company.query.count(),
        'companies': companies
    }), 200


def create_company():
    # If data is empty or there is no field
    if not (request.json and 'name' in request.json):
        abort(400)

    company = Company(
        name=request.json['name'],
        bio=request.json['bio'],
        website=request.json['website'],
    )

    try:
        company.save()
    except IntegrityError:
        return jsonify({
            'status': 'failure',
            'message': 'company already exists'
        }), 400

    # if user sends founder list
    if 'founders' in request.json:
        for founder in request.json['founders']:
            Founder(
                company_id=company.id,
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


@companies_blueprint.route('/companies', methods=['GET', 'POST'])
def companies():
    """GET to retrieve all the companies
    POST to create a new company
    """
    if request.method == 'GET':
        return get_all_companies()
    elif request.method == 'POST':
        return create_company()
    else:
        return 405


@companies_blueprint.route('/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    data = {
        'id': company.id,
        'name': company.name,
        'website': company.website,
        'founders': list(map(
            lambda founder: {
                'name': founder.name,
                'email': founder.email,
                'role': founder.role,
            },
            list(company.founders)
        )),
        'bio': company.bio
    }
    return jsonify(data)


@companies_blueprint.route('/companies/<int:company_id>', methods=['POST'])
def post_company(company_id):
    if not request.json:
        return jsonify({
            'status': 'failure',
            'message': 'empty metrics'
        }), 400

    for metric in request.json:
        if request.json[metric] == '':
            return jsonify({
                'status': 'failure',
                'message': 'one of the metrics is empty'
            }), 400

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    response_data = {
        'metrics_added': {}
    }

    for metric in request.json:
        KPI[metric](
            company_id=company_id,
            value=request.json[metric]
        ).save()
        response_data['metrics_added'][metric] = request.json[metric]

    response_data['status'] = 'success'
    response_data['message'] = 'metrics added'

    return jsonify(response_data), 200
