# server/app/apis/auth.py

from flask import (
    jsonify,
    request,
)

from app import bcrypt
from app.apis import auth_blueprint as auth
from app.models import User


def protected_route(fn):
    """Function decorator to wrap around protected endpoints"""
    def protected_fn(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] if auth_header else ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)

            # if resp is an integer, that means it's a user id
            if not isinstance(resp, str):
                return fn(*args, **kwargs, resp=resp)

            return jsonify({
                'status': 'failure',
                'message': resp
            }), 500
        else:
            return jsonify({
                'status': 'failure',
                'message': 'unauthorized'
            }), 401

    protected_fn.__name__ = fn.__name__
    return protected_fn


@auth.route('/auth/register', methods=['POST'])
def register():
    # empty request
    # request that does not contain either email or password
    # email or password field is empty
    if not request.json or ('email' and 'password') not in request.json \
        or not (request.json.get('email') != ''
                and request.json.get('password') != ''):
        return jsonify({
            'status': 'failure',
            'message': 'invalid register request'
        }), 400

    name = request.json.get('name')
    email = request.json['email']
    password = request.json['password']
    staff = True if request.json.get('staff') == 'True' else False

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            'status': 'failure',
            'message': 'user exists. log in instead',
        }), 202
    else:
        user = User(email=email, name=name, password=password, staff=staff)
        user.save()
        auth_token = user.encode_auth_token(user.id)
        return jsonify({
            'status': 'success',
            'message': 'successfully registered',
            'auth_token': auth_token.decode(),
        }), 201


@auth.route('/auth/login', methods=['POST'])
def login():
    # empty request
    # request that does not contain either email or password
    # email or password field is empty
    if not request.json or ('email' and 'password') not in request.json \
        or not (request.json.get('email') != ''
                and request.json.get('password') != ''):
        return jsonify({
            'status': 'failure',
            'message': 'invalid login request'
        }), 400

    email = request.json['email']
    password = request.json['password']

    try:
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(
            user.password, password
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return jsonify({
                    'status': 'success',
                    'message': 'successfully logged in',
                    'auth_token': auth_token.decode()
                }), 200
        else:
            return jsonify({
                'status': 'failure',
                'message': 'wrong password or user does not exist'
            }), 404
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'failure',
            'message': 'internal server error'
        }), 500


@auth.route('/auth/logout', methods=['POST'])
@protected_route
def logout(resp=None):
    pass


@auth.route('/auth/status', methods=['GET'])
@protected_route
def user_status(resp=None):
    user = User.query.get(resp)
    return jsonify({
        'status': 'success',
        'data': {
            'user_id': user.id,
            'email': user.email,
            'company': user.founder_info.company.name
            if user.founder_info else 'The Brandery',
            'registered_on': user.registered_on,
            'staff': user.staff,
        }
    }), 200
