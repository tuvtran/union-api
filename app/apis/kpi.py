# server/app/apis/kpi.py

import datetime
from flask import (
    jsonify,
    request,
)

from typing import Dict, Any, Tuple

from app import db
from app.apis import kpi_blueprint as kpi
from app.apis.auth import protected_route
from app.models import User, Company, BaseMetric

KPI: Dict[str, Any] = {}
for Metric in BaseMetric.__subclasses__():
    KPI[Metric.__tablename__] = Metric


def get_kpi_for_company(company_id) -> Dict[str, Any]:
    # default time before adding new metrics
    default_time = datetime.datetime.utcnow() - datetime.timedelta(days=10)
    metric_field = {}

    for metric in KPI:
        kpi_query = KPI[metric].query.filter_by(company_id=company_id)
        total_weeks = kpi_query.count()
        values = kpi_query.order_by(KPI[metric].week).all()
        last_updated = KPI[metric].get_last_updated(company_id).updated_at \
            if KPI[metric].get_last_updated(company_id) else default_time

        metric_field[metric] = {
            'weeks': total_weeks,
            'last_updated': last_updated,
            'data': list(map(
                lambda value: value.value,
                values
            ))
        }

    return metric_field


@kpi.route('/metrics', methods=['GET'])
@protected_route
def get_metrics_list(resp: int = None) -> Tuple[object, int]:
    if not User.query.get(resp):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

    response_obj = {}

    # go through every subclass of BaseMetric
    # and get the custom name
    for Metric in BaseMetric.__subclasses__():
        response_obj[Metric.__tablename__] = {
            'name': Metric.get_custom_name()
        }

    return jsonify(response_obj), 200


@kpi.route('/companies/<int:company_id>', methods=['POST'])
@protected_route
def post_company(company_id: int, resp: int = None) -> Tuple[object, int]:
    user = User.query.get(resp)
    if not user.staff \
        and (not user.founder_info
             or user.founder_info.company_id != company_id):
        return jsonify({
            'status': 'failure',
            'message': 'user not authorized to this view'
        }), 401

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

    response_data: Dict[str, Any] = {
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

    return jsonify(response_data), 201


@kpi.route('/companies/<int:company_id>/metrics', methods=['GET'])
@protected_route
def get_metrics(company_id: int, resp: int = None) -> Tuple[object, int]:
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

    response_obj = get_kpi_for_company(company_id)

    return jsonify(response_obj), 200


@kpi.route('/companies/<int:company_id>/metrics', methods=['PUT'])
@protected_route
def put_metric(company_id: int, resp: int = None) -> Tuple[object, int]:
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

    for metric in request.json:
        # if there is no data in the database
        if KPI[metric].query.count() == 0:
            return jsonify({
                'status': 'failure',
                'message': 'there is no data to update'
            }), 400

    for metric in request.json:
        KPI[metric].get_last_updated(company_id).value = request.json[metric]
        db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'resource updated'
    }), 200
