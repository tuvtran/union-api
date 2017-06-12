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
