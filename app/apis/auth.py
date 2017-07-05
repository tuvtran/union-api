# server/app/apis/auth.py

from flask import (
    jsonify,
    request,
)

import os
from typing import Callable, Any, Tuple
from app import bcrypt, db
from app.apis import auth_blueprint as auth
from app.models import User


def protected_route(fn: Callable[..., object]) -> Callable:
    """Function decorator to wrap around protected endpoints"""
    def protected_fn(*args: Any, **kwargs: Any):
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
def register() -> Tuple[object, int]:
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

    name: str = request.json.get('name')
    email: str = request.json['email']
    password: str = request.json['password']
    staff: bool = True if request.json.get('staff') else False

    user: User = User.query.filter_by(email=email).first()
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
def login() -> Tuple[object, int]:
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
                    'auth_token': auth_token.decode(),
                    'company_id': user.founder_info.company_id
                    if user.founder_info else 0,
                    'company': user.founder_info.company.name
                    if user.founder_info else 'The Brandery',
                    'registered_on': user.registered_on,
                    'staff': user.staff,
                }), 200
            else:
                return jsonify({
                    'status': 'failure',
                    'message': 'internal server error'
                }), 500
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
def logout(resp: int = None):
    pass


@auth.route('/auth/status', methods=['GET'])
@protected_route
def user_status(resp: int = None) -> Tuple[object, int]:
    user: User = User.query.get(resp)
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


@auth.route('/auth/change', methods=['PUT'])
@protected_route
def change(resp: int = None) -> Tuple[object, int]:
    user: User = User.query.get(resp)

    new_email: str = request.json['new_email']
    old_password: str = request.json['old_password']
    new_password: str = request.json['new_password']

    if bcrypt.check_password_hash(user.password, old_password):
        user.password = bcrypt.generate_password_hash(
            new_password, os.environ.get('BCRYPT_LOG_ROUNDS', 4)
        ).decode()
        if new_email != user.email:
            user.email = new_email
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'successfully changed login information'
        }), 200
    else:
        return jsonify({
            'status': 'failure',
            'message': 'old password is incorrect'
        }), 400
