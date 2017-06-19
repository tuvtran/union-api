# server/app/models.py

import os
import jwt
import datetime
from app import db, bcrypt
from flask import current_app
from sqlalchemy.ext.declarative import declared_attr


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
    user_info = db.relationship('User', backref='founder_info')

    def __repr__(self):
        return f'<{self.name} ({self.role}) - {self.email}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

        User(
            name=self.name, email=self.email,
            founder_id=self.id, password="founder").save()


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    founder_id = db.Column(
        db.Integer, db.ForeignKey('founders.id')
    )
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp())
    staff = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User: {self.email}>'

    def save(self):
        self.password = bcrypt.generate_password_hash(
            self.password, os.environ.get('BCRYPT_LOG_ROUNDS', 4)
        ).decode()

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


class BaseMetric(db.Model):

    __abstract__ = True

    @declared_attr
    def company_id(cls):
        return db.Column(db.Integer, db.ForeignKey('companies.id'))

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def save(self):
        last = self.__class__.query.filter_by(company_id=self.company_id)\
            .order_by(self.__class__.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_last_updated(cls, company_id):
        """Return a data point that is last updated/created"""
        return cls.query.filter_by(company_id=company_id)\
            .order_by(cls.updated_at.desc()).first()


class Sale(BaseMetric):

    __tablename__ = 'sales'


class Customer(BaseMetric):

    __tablename__ = 'customers'


class Traffic(BaseMetric):

    __tablename__ = 'traffic'


class Email(BaseMetric):

    __tablename__ = 'emails'
