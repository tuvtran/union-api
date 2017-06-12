# server/app/models.py

from app import db


class Company(db.Model):

    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    founders = db.relationship('Founder', backref='company', lazy='dynamic')
    website = db.Column(db.String(255), nullable=False, unique=True)
    bio = db.Column(db.Text)

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


class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)


class Traffic(db.Model):

    __tablename__ = 'traffic'
    id = db.Column(db.Integer, primary_key=True)


class Email(db.Model):

    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
