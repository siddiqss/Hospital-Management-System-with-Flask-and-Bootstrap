from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from backend import app, db
from backend.forms import LoginForm, RegistrationForm, PatientRegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from backend.models import Employee, Patient, Appointments
from backend.read_data import read_patient_data
import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Hospital Management Portal')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        emp = Employee.query.filter_by(email=form.email.data).first()
        if emp is None or not emp.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(emp, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        emp = Employee(email=form.email.data, name=form.name.data, address=form.address.data, role=form.role.data)
        emp.set_password(form.password.data)
        db.session.add(emp)
        db.session.commit()
        flash('New employee registered!', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register an Employee', form=form)

@app.route('/user/<id>')
@login_required
def emp(id):
    emp = Employee.query.filter_by(id=id).first_or_404()
    return render_template('_employee.html', emp=emp, title='Profile')

@app.route('/all')
@login_required
def all_employees():
    emps = Employee.query.all()
    return render_template('employees.html',emps=emps, title='All Employees')

@app.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        patient = Patient(email=form.email.data, name=form.name.data, age=form.age.data, temperature=form.temperature.data, pulse=form.pulse.data, lat_pos=form.lat_pos.data, lng_pos=form.lng_pos.data, timestamp=datetime.datetime.now())
        db.session.add(patient)
        db.session.commit()
        flash('New patient registered!', 'info')
        return redirect(url_for('index'))
    return render_template('register_patient.html', title='Register Patient', form=form)

@app.route('/patient/<int:id>')
@login_required
def pat(id):
    pat_id_data, temp_data, pulse_data, lat_pos, lng_pos, timestamp_data = read_patient_data()
    pat_id_data = int(pat_id_data)
    temp_data = float(temp_data)
    pulse_data = int(pulse_data)
    lat_pos = float(lat_pos)
    lng_pos = float(lng_pos)
    timestamp_data = datetime.datetime.fromtimestamp(float(timestamp_data))
    patient = Patient.query.filter_by(id=id).first_or_404()
    print(type(pat_id_data), type(temp_data), type(pulse_data), type(lat_pos), type(lng_pos), type(timestamp_data))
    print(type(patient.id), type(patient.temperature), type(patient.pulse), type(patient.lat_pos), type(patient.lng_pos), type(patient.timestamp))
    if pat_id_data == id:
        if temp_data != patient.temperature and pulse_data != patient.pulse and lat_pos != patient.lat_pos and lng_pos != patient.lng_pos:
            patient.temperature = temp_data
            patient.pulse = pulse_data
            patient.lat_pos = lat_pos
            patient.lng_pos = lng_pos
            patient.previous_data = f'{patient.previous_data};{temp_data};{pulse_data};{lat_pos};{lng_pos};{timestamp_data}'
            db.session.commit()
    print(patient.previous_data)
    if patient.previous_data is None:
        temp = 'No previous data'
        return render_template('_patient.html', all_temp_data=temp, all_pulse_data=temp,
                               all_lat_pos_data=temp, all_lng_pos_data=temp,
                               all_timestamp_data=temp, pat=patient, title='Patient Profile')
    else:
        prev_data_arr = patient.previous_data.split(';')
        prev_data_arr.remove('None')
        if len(prev_data_arr) == 0:
            i = 0
            while i<4:
                prev_data_arr.append('No previous data')
                i+=1
        all_temp_data = [prev_data_arr[i] for i in range(0, len(prev_data_arr),5)]
        all_pulse_data = [prev_data_arr[j] for j in range(1, len(prev_data_arr),5)]
        all_lat_pos_data = [prev_data_arr[k] for k in range(2, len(prev_data_arr),5)]
        all_lng_pos_data = [prev_data_arr[l] for l in range(3, len(prev_data_arr),5)]
        all_timestamp_data = [prev_data_arr[m] for m in range(4, len(prev_data_arr),5)]
        print(all_temp_data, all_pulse_data, all_lat_pos_data, all_lng_pos_data, all_timestamp_data)

        return render_template('_patient.html', all_temp_data=all_temp_data, all_pulse_data=all_pulse_data, all_lat_pos_data=all_lat_pos_data, all_lng_pos_data=all_lng_pos_data, all_timestamp_data=all_timestamp_data, pat=patient, title='Patient Profile')

@app.route('/all_patients')
@login_required
def all_patients():
    pats = Patient.query.order_by(Patient.id.desc()).all()
    return render_template('patients.html', pats=pats, title='All Patients')

# @app.route('/appointment/add/', methods=['GET', 'POST'])
# @login_required
# def appointments(id):
#     pat = Patient.query.filter_by(id=id).first_or_404()
#     temperature = random.randint(97, 104)
#     posture = random.uniform(29.1, 40.1)
#     pulse = random.randint(60, 100)
#     time = datetime.datetime(2015, 6, 5, 8, 10, 10)
#     completed = False
#     appointment = Appointments(name=pat.name, age=pat.age, temperature=temperature, pulse=pulse, posture=posture, completed=completed, time=time)
#     db.session.add(appointment)
#     db.session.commit()
#     flash('New appointment added!', 'info')
#     return render_template('appointment.html', pat=pat, temperature=temperature, pulse=pulse, posture=posture, completed=completed, time=time, title = 'Make an Appointment')

@app.route('/appointment/<id>', methods=['GET', 'POST'])
@login_required
def view_appointments(id):
    pat = Patient.query.filter_by(id=id).first_or_404()
    apps = Appointments.query.filter_by(name=pat.name).first_or_404()
    return render_template('view_appointment.html', pat=pat, apps=apps, title = 'Patient\'s Appointments')


@app.route('/all_appointments/')
@login_required
def all_appointments():
    pat_id_data, temp_data, pulse_data, lat_data, lng_data, timestamp_data = read_patient_data()
    pat_id_data = int(pat_id_data)
    temp_data = float(temp_data)
    pulse_data = int(pulse_data)
    lat_data = float(lat_data)
    lng_data = float(lng_data)
    print(timestamp_data)
    timestamp_data = datetime.datetime.fromisoformat(timestamp_data)
    patient = Patient.query.filter_by(id=pat_id_data).first_or_404()
    ap = Appointments.query.filter_by(name=patient.name).first()

    if ap is None:
        if float(temp_data) > 99 or int(pulse_data) > 100 or int(pulse_data) < 60:
            completed = False
            appointment = Appointments(name=patient.name, age=patient.age, temperature=temp_data, pulse=pulse_data,
                                       lat_pos=lat_data, lng_pos=lng_data,
                                       completed=completed, time=timestamp_data)
            db.session.add(appointment)
            db.session.commit()
    appointments = Appointments.query.order_by(Appointments.id.desc()).all()
    return render_template('appointments.html', appointments=appointments, title='All Appointments')






