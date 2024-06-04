from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from dbfunc import getConnection, insert_booking, get_available_slots, get_password_hash, get_service_by_id, get_booking_by_id, get_slot_by_id, get_available_slots, insert_booking, get_password_hash, get_services, get_slots, get_bookings, insert_service, update_service, delete_service, insert_slot, update_slot, delete_slot, insert_booking, update_booking, delete_booking
import random
import string
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


app = Flask(__name__)
app.secret_key = '1407'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lapassionduzenbys@gmail.com'
app.config['MAIL_PASSWORD'] = 'xndr mhdg nacz ytcq'
app.config['MAIL_DEFAULT_SENDER'] = 'lapassionduzenbys@gmail.com'

mail = Mail(app)
bcrypt = Bcrypt(app)

def generate_reference():
    """Generate a unique reference number for the booking."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/a-propos')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('we-do.html')

@app.route('/tarifs')
def tarifs():
    return render_template('pricing.html')

@app.route('/contactez-nous')
def contact():
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Hash the password
        password_hash = generate_password_hash(password)

        # Insert the user into the database
        conn = getConnection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO users (first_name, last_name, email, phone, password_hash, created_at) VALUES (%s, %s, %s, %s, %s, NOW())"
                data = (first_name, last_name, email, phone, password_hash)
                cursor.execute(query, data)
                conn.commit()
                flash('User registered successfully!', 'success')
                return redirect(url_for('login'))
            except mysql.connector.Error as err:
                print("Error inserting user:", err)
                conn.rollback()
                flash('Error registering user.', 'error')
            finally:
                cursor.close()
                conn.close()
    return render_template('register.html')

@app.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Get the stored password hash from the database
        password_hash = get_password_hash(email)

        if password_hash and check_password_hash(password_hash, password):
            # Password is correct, set the session
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')




# @app.route('/reservation', methods=['GET', 'POST'])
# def booking():
#     if request.method == 'GET':
#         slots = get_available_slots()  # Fetch available slots from the database
#         return render_template('booking.html', slots=slots)
#     elif request.method == 'POST':
#         full_name = request.form['full_name']
#         email = request.form['email']
#         phone = request.form['phone']
#         slot_id = request.form['slot_id']
#         message = request.form['message']

#         # Generate a unique reference number
#         reference_number = generate_reference()

#         # Insert the booking information into the database
#         insert_booking(full_name, email, phone, slot_id, message, reference_number)

#         # Flash a success message
#         flash('Your reservation was successful!', 'success')

#         # Redirect to the confirmation page with the email and reference number as query parameters
#         return redirect(url_for('send_email', email=email, reference_number=reference_number))




@app.route('/reservation', methods=['GET', 'POST'])
def booking():
    if request.method == 'GET':
        slots = get_available_slots()  # Fetch available slots from the database
        return render_template('booking.html', slots=slots)
    elif request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        slot_id = request.form['slot_id']
        message = request.form['message']

        # Generate a unique reference number
        reference_number = generate_reference()

        try:
            # Insert the booking information into the database
            insert_booking(full_name, email, phone, slot_id, message, reference_number)

            # Flash a success message
            flash('Your reservation was successful!', 'success')

            # Redirect to the confirmation page with the email and reference number as query parameters
            return redirect(url_for('send_email', email=email, reference_number=reference_number))
        except Exception as e:
            print("Error inserting booking:", e)
            flash('Error making reservation.', 'error')
            return redirect(url_for('booking'))



@app.route('/confirmation')
def confirmation():
    # Retrieve booking information from the query parameters
    email = request.args.get('email')
    reference_number = request.args.get('reference_number')
    
    return render_template('confirmation.html', 
                           email=email,
                           reference_number=reference_number)

@app.route('/confirmation/mail')
def send_email():
    # Get the email and reference number from the query parameters
    email = request.args.get('email')
    reference_number = request.args.get('reference_number')

    if email and reference_number:
        msg = Message('Booking Confirmation', recipients=[email])
        msg.body = f'This is a confirmation email for your booking. Your reference number is {reference_number}. Thank you!'
        mail.send(msg)
        return render_template('confirmation.html', email=email, reference_number=reference_number)
    else:
        flash('Email address or reference number is missing.', 'error')
        return redirect(url_for('booking'))

@app.route('/admin')
def admin_dashboard():
    if 'logged_in' in session and session['logged_in']:
        services = get_services()
        slots = get_slots()
        bookings = get_bookings()
        return render_template('admin_dashboard.html', services=services, slots=slots, bookings=bookings)
    else:
        return redirect(url_for('index'))

@app.route('/admin/service/add', methods=['POST'])
def add_service():
    service_name = request.form['service_name']
    description = request.form['description']
    duration = request.form['duration']
    price = request.form['price']
    insert_service(service_name, description, duration, price)
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/service/update/<int:service_id>', methods=['POST'])
def update_service_route(service_id):
    service_name = request.form['service_name']
    description = request.form['description']
    duration = request.form['duration']
    price = request.form['price']
    update_service(service_id, service_name, description, duration, price)
    flash('Service updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/service/delete/<int:service_id>', methods=['POST'])
def delete_service_route(service_id):
    delete_service(service_id)
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/slot/add', methods=['POST'])
def add_slot():
    service_id = request.form['service_id']
    slot_date = request.form['slot_date']
    slot_time = request.form['slot_time']
    available = request.form['available']
    insert_slot(service_id, slot_date, slot_time, available)
    flash('Slot added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/slot/update/<int:slot_id>', methods=['POST'])
def update_slot_route(slot_id):
    service_id = request.form['service_id']
    slot_date = request.form['slot_date']
    slot_time = request.form['slot_time']
    available = request.form['available']
    update_slot(slot_id, service_id, slot_date, slot_time, available)
    flash('Slot updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/slot/delete/<int:slot_id>', methods=['POST'])
def delete_slot_route(slot_id):
    delete_slot(slot_id)
    flash('Slot deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/delete/<int:booking_id>', methods=['POST'])
def delete_booking_route(booking_id):
    delete_booking(booking_id)
    flash('Booking deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=False, host ='0.0.0.0')
