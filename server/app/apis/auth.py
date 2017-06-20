# server/app/apis/auth.py

from flask import (
    jsonify,
    request,
)

from app import bcrypt
from app.apis import auth_blueprint as auth
from app.models import User


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

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            'status': 'failure',
            'message': 'user exists. log in instead',
        }), 202
    else:
        user = User(email=email, name=name, password=password)
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
