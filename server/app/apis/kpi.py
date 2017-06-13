from flask import (
    jsonify,
    request,
)

from app.apis import kpi_blueprint
from app.models import (
    Company,
    Sale,
    Customer,
    Traffic,
    Email
)

KPI = {
    'sales': Sale,
    'customers': Customer,
    'traffic': Traffic,
    'emails': Email
}


@kpi_blueprint.route('/companies/<int:company_id>', methods=['POST'])
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


@kpi_blueprint.route('/companies/<int:company_id>/sales', methods=['GET'])
def get_sales(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    total_weeks = Sale.query.filter_by(company_id=company_id).count()
    sales = Sale.query.filter_by(company_id=company_id).order_by(Sale.week).all()

    return jsonify({
        'weeks': total_weeks,
        'data': list(map(
            lambda sale: sale.value,
            sales
        ))
    })


@kpi_blueprint.route('/companies/<int:company_id>/customers', methods=['GET'])
def get_customers(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    total_weeks = Customer.query.filter_by(company_id=company_id).count()
    customers = Customer.query.filter_by(company_id=company_id).order_by(Customer.week)

    return jsonify({
        'weeks': total_weeks,
        'data': list(map(
            lambda customer: customer.value,
            customers
        ))
    })


@kpi_blueprint.route('/companies/<int:company_id>/traffic', methods=['GET'])
def get_traffic(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    total_weeks = Traffic.query.filter_by(company_id=company_id).count()
    traffic = Traffic.query.filter_by(company_id=company_id).order_by(Traffic.week)

    return jsonify({
        'weeks': total_weeks,
        'data': list(map(
            lambda traff: traff.value,
            traffic
        ))
    })


@kpi_blueprint.route('/companies/<int:company_id>/emails', methods=['GET'])
def get_emails(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    total_weeks = Email.query.filter_by(company_id=company_id).count()
    emails = Email.query.filter_by(company_id=company_id).order_by(Email.week)

    return jsonify({
        'weeks': total_weeks,
        'data': list(map(
            lambda email: email.value,
            emails
        ))
    })