# server/app/views.py

from flask import (
    jsonify,
    request,
    make_response,
    abort
)
from sqlalchemy.exc import IntegrityError

from app import db
from app.apis import companies_blueprint as company
from app.apis.kpi import get_kpi_for_company
from app.apis.auth import protected_route
from app.models import Company, Founder, User


def get_all_companies():
    companies = {}
    for startup in Company.query.all():
        companies[startup.name] = {
            'id': startup.id,
            'website': startup.website,
            'bio': startup.bio,
            'founders': list(map(
                lambda founder: {
                    'name': founder.name,
                    'email': founder.email,
                    'role': founder.role
                },
                startup.founders
            )),
            'metrics': get_kpi_for_company(startup.id)
        }

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
        db.session.rollback()
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


@company.route('/companies', methods=['GET', 'POST'])
@protected_route
def companies(resp=None):
    """GET to retrieve all the companies
    POST to create a new company
    """
    user = User.query.get(resp)
    if not user.staff:
        return jsonify({
            'status': 'failure',
            'message': 'non-staff members not allowed'
        }), 401

    if request.method == 'GET':
        return get_all_companies()
    elif request.method == 'POST':
        return create_company()
    else:
        return 405


@company.route('/companies/<int:company_id>', methods=['PUT'])
@protected_route
def update_companies(company_id, resp=None):
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

    company = Company.query.get(company_id)

    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404


@company.route('/companies/<int:company_id>', methods=['GET'])
@protected_route
def get_company(company_id, resp=None):
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

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

    data['metrics'] = get_kpi_for_company(company_id)

    return jsonify(data), 200
