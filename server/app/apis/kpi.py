from flask import (
    jsonify,
    request,
)

from app.apis import kpi_blueprint as kpi
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


@kpi.route('/companies/<int:company_id>', methods=['POST'])
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


@kpi.route('/companies/<int:company_id>/<string:metric>', methods=['GET'])
def get_metric(company_id, metric):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({
            'status': 'failure',
            'message': 'company not found'
        }), 404

    if metric not in KPI:
        return jsonify({
            'status': 'failure',
            'message': 'metric does not exist'
        }), 404

    kpi_query = KPI[metric].query.filter_by(company_id=company_id)
    total_weeks = kpi_query.count()
    values = kpi_query.order_by(KPI[metric].week).all()
    last_updated = KPI[metric].get_last_updated(company_id).updated_at

    return jsonify({
        'weeks': total_weeks,
        'last_updated': last_updated,
        'data': list(map(
            lambda value: value.value,
            values
        ))
    })
