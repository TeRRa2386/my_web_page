from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap5 import Bootstrap
from datetime import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SK')
Bootstrap(app)

EMAIL = os.getenv('EM')
EMAIL_PASS = os.getenv('EMP')

class HiForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    send = SubmitField('Send')


def today_year():
    today = dt.now().year
    return today

def send_message(first, last, email, message):
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASS)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f'Subject:{first} say Hi!\n\n'
                f'{first} {last} send you this message:\n\n'
                f'{message}\n\n'
                f'email: {email}'
        )

@app.route('/')
def home():
    time = today_year()
    return render_template('index.html', time=time)

@app.route('/hi', methods=['GET', 'POST'])
def contact():
    form = HiForm()
    if form.validate_on_submit():
        send_message(first=form.first.data, last=form.last.data, message=form.message.data, email=form.email.data)
        flash("✅ Your message was sent successfully. Thank you!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)