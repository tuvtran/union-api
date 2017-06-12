# server/app/models.py

from app import db


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


class Sale(db.Model):

    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Float, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Traffic(db.Model):

    __tablename__ = 'traffic'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Email(db.Model):

    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    value = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
