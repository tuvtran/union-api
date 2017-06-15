# server/app/models.py

import os
import jwt
import datetime
from flask import current_app
from app import db, bcrypt


class Company(db.Model):

    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    website = db.Column(db.String(255), nullable=False, unique=True)
    bio = db.Column(db.Text)

    founders = db.relationship('Founder', backref='company', lazy='dynamic')
    sales = db.relationship('Sale', backref='company', lazy='dynamic')
    customers = db.relationship('Customer', backref='company', lazy='dynamic')
    traffic = db.relationship('Traffic', backref='company', lazy='dynamic')
    emails = db.relationship('Email', backref='company', lazy='dynamic')

    def __repr__(self):
        return f'<Company: {self.name}, Website: {self.website}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Founder(db.Model):

    __tablename__ = 'founders'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(255))
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )
    role = db.Column(db.String(255))
    user = db.relationship('User', backref='founder_info')

    def __repr__(self):
        return f'<Founder: {self.name} ({self.role}) - {self.email})>'

    def save(self):
        db.session.add(self)
        db.session.commit()

        User(email=self.email, founder_id=self.id).save()


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    founder_id = db.Column(
        db.Integer, db.ForeignKey('founders.id'))
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(
        db.String(255), nullable=True,
        default=bcrypt.generate_password_hash(
            '123456', os.environ.get('BCRYPT_LOG_ROUNDS', 4)
        ).decode())
    registered_on = db.Column(
        db.DateTime, nullable=False,
        default=datetime.datetime.now())
    staff = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User: {self.email}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() +
                datetime.timedelta(days=0, minutes=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config['SECRET'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Sale(db.Model):

    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Float, nullable=False)
    week = db.Column(db.Integer, nullable=False)

    def save(self):
        last = Sale.query.filter_by(company_id=self.company_id)\
            .order_by(Sale.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()


class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)

    def save(self):
        last = Customer.query.filter_by(company_id=self.company_id)\
            .order_by(Customer.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()


class Traffic(db.Model):

    __tablename__ = 'traffic'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)

    def save(self):
        last = Traffic.query.filter_by(company_id=self.company_id)\
            .order_by(Traffic.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()


class Email(db.Model):

    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)
    week = db.Column(db.Integer, nullable=False)

    def save(self):
        last = Email.query.filter_by(company_id=self.company_id)\
            .order_by(Email.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()
