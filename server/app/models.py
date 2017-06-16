# server/app/models.py

from app import db
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

    def __repr__(self):
        return f'<{self.name} ({self.role}) - {self.email}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


class BaseMetric(db.Model):

    __abstract__ = True

    @declared_attr
    def company_id(cls):
        return db.Column(db.Integer, db.ForeignKey('companies.id'))

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    week = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp())

    def save(self):
        last = self.__class__.query.filter_by(company_id=self.company_id)\
            .order_by(self.__class__.week.desc()).first()
        self.week = last.week + 1 if last else 0

        db.session.add(self)
        db.session.commit()

    @classmethod
    def last_updated(cls, company_id):
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
