
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import dbfunc
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '1407'

app = Flask(__name__)

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

@app.route('/connexion')
def login():
    return render_template('login.html')


@app.route('/reservation/<int:service_id>')
def booking(service_id):
    return render_template('booking.html')




if __name__ == '__main__':
    app.run(debug=True)
