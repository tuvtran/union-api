# server/app/apis/auth.py

from flask import request, jsonify

from app import bcrypt
from app.models import User
from app.apis import auth_blueprint as auth


def protected_route(fn):
    def protected_fn(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return fn(*args, **kwargs, resp=resp)

            return jsonify({
                'status': 'failure',
                'message': resp
            })
        else:
            return jsonify({
                'status': 'failure',
                'message': 'provide a valid auth token'
            }), 401

    protected_fn.__name__ = fn.__name__
    return protected_fn


@auth.route('/auth/login', methods=['POST'])
def post():
    post_data = request.get_json()
    try:
        user = User.query.filter_by(
            email=post_data.get('email')
        ).first()

        if user and bcrypt.check_password_hash(
            user.password, post_data.get('password')
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_obj = {
                    'status': 'success',
                    'message': 'successfully logged in',
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_obj), 200
        else:
            response_obj = {
                'status': 'failure',
                'message': 'user does not exist'
            }
            return jsonify(response_obj), 404

    except Exception as e:
        print(e)
        response_obj = {
            'status': 'failure',
            'message': 'try again'
        }
        return jsonify(response_obj), 500


@auth.route('/auth/status', methods=['GET'])
@protected_route
def user_status(resp=None):
    user = User.query.get(resp)
    response_obj = {
        'status': 'success',
        'data': {
            'user_id': user.id,
            'email': user.email,
            'company': user.founder_info.company.name
            if user.founder_info else 'The Brandery',
            'registered_on': user.registered_on,
            'staff': user.staff,
        }
    }
    return jsonify(response_obj), 200
