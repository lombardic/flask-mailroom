import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/donations/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Check to see if the name already exists in the database.
        if Donor.select().where(Donor.name == request.form['name']).exists():
            name = Donor.select().where(Donor.name == request.form['name']).get()
            donation = Donation(donor=name, value=int(request.form['amount'])).save()

            return redirect(url_for('all'))

        else:
            return render_template('create.jinja2', error="No donor in database")

    else:
        # Display the add donation page.
        return render_template('create.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
