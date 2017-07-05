# server/app/models.py

import os
import abc
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
    traffic = db.relationship('Traffic', backref='company', lazy='dynamic')
    active_users = db.relationship('ActiveUser', backref='company', lazy='dynamic')
    paying_users = db.relationship('PayingUser', backref='company', lazy='dynamic')
    subscribers = db.relationship('Subscriber', backref='company', lazy='dynamic')
    engagement = db.relationship('Engagement', backref='company', lazy='dynamic')
    pilots = db.relationship('Pilot', backref='company', lazy='dynamic')
    product_releases = db.relationship('ProductRelease', backref='company', lazy='dynamic')
    preorders = db.relationship('Preorder', backref='company', lazy='dynamic')
    automation_percents = db.relationship('AutomationPercentage', backref='company', lazy='dynamic')
    cpa = db.relationship('CPA', backref='company', lazy='dynamic')
    conversion_rate = db.relationship('ConversionRate', backref='company', lazy='dynamic')
    marketing_spent = db.relationship('MarketingSpent', backref='company', lazy='dynamic')
    other_1 = db.relationship('Other1', backref='company', lazy='dynamic')
    other_2 = db.relationship('Other2', backref='company', lazy='dynamic')
    mrr = db.relationship('MRR', backref='company', lazy='dynamic')

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
                datetime.timedelta(days=0, seconds=current_app.config['EXP']),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        @params: authentication token to decode
        @return: integer/string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again"


class BaseMetric(db.Model):

    __abstract__ = True
    __metaclass__ = abc.ABCMeta

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
    def get_last_updated(cls, company_id: int) -> object:
        """Return a data point that is last updated/created"""
        return cls.query.filter_by(company_id=company_id)\
            .order_by(cls.updated_at.desc()).first()

    @abc.abstractclassmethod
    def get_custom_name(cls) -> str:
        """Return a user-friendly name"""
        ...


class Sale(BaseMetric):

    __tablename__ = 'sales'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Sales'


class Traffic(BaseMetric):

    __tablename__ = 'traffic'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Traffic'


class ActiveUser(BaseMetric):

    __tablename__ = 'active_users'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Active users'


class PayingUser(BaseMetric):

    __tablename__ = 'paying_users'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Paying users'


class Subscriber(BaseMetric):

    __tablename__ = 'subscribers'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Subscribers'


class Engagement(BaseMetric):

    __tablename__ = 'engagement'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Engagement'


class MRR(BaseMetric):

    __tablename__ = 'mrr'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Revenue'


class Pilot(BaseMetric):

    __tablename__ = 'pilots'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Pilots'


class ProductRelease(BaseMetric):

    __tablename__ = 'product_releases'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Product releases'


class Preorder(BaseMetric):

    __tablename__ = 'preorders'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Preorders'


class AutomationPercentage(BaseMetric):

    __tablename__ = 'automation_percents'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Percents of automation'


class CPA(BaseMetric):

    __tablename__ = 'cpa'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Cost per acquisition'


class ConversionRate(BaseMetric):

    __tablename__ = 'conversion_rate'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Conversion rate'


class MarketingSpent(BaseMetric):

    __tablename__ = 'marketing_spent'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Marketing spent'


class Other1(BaseMetric):

    __tablename__ = 'other_1'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Other metric 1'


class Other2(BaseMetric):

    __tablename__ = 'other_2'

    @classmethod
    def get_custom_name(cls) -> str:
        return 'Other metric 2'
