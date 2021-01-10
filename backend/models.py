from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from backend import login
from hashlib import md5

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(120))
    role = db.Column(db.String(10))
    address = db.Column(db.String(200))
    patients = db.relationship('Patient', backref='employee', lazy='dynamic')

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee Email {}>'.format(self.email)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    pulse = db.Column(db.Integer)
    lat_pos = db.Column(db.Float)
    lng_pos = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    previous_data = db.Column(db.String)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<Patient Email {}>'.format(self.email)


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    pulse = db.Column(db.Integer)
    lat_pos = db.Column(db.Float)
    lng_pos = db.Column(db.Float)
    time = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    def __repr__(self):
        return '<Appointment ID {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))