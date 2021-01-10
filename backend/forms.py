from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, optional, length, number_range
from backend.models import Employee, Patient

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    address = TextAreaField('Address', [optional(), length(max=200)])
    role = SelectField(u'Role', choices=[('Dr.', 'Doctor'), ('N', 'Nurse'), ('C', 'Caretaker')])
    submit = SubmitField('Register')


    def validate_email(self, email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp is not None:
            raise ValidationError('Please use a different email address.')

class PatientRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired(), number_range(1,100)])
    temperature = FloatField('Temperature')
    pulse = IntegerField('Pulse rate')
    lat_pos = FloatField('Latitude')
    lng_pos = FloatField('Longitude')
    submit = SubmitField('Register Patient')


    def validate_email(self, email):
        pat = Patient.query.filter_by(email=email.data).first()
        if pat is not None:
            raise ValidationError('Please use a different email address.')


