from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
##app.config['SQL_URI']
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'


## database declarations
class Item(db.Model):
    i_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    seller = db.Column(db.Integer, db.ForeignKey('User.u_id'), nullable = False)
    category_1 = db.Column(db.String(50), nullable=False)
    category_2 = db.Column(db.String(50))
    category_3 = db.Column(db.String(50))
    price = db.Column(db.Double(2), nullable=False)
    condition = db.Column(db.String(50))
    listing_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sold = db.Column(db.Boolean)
    exchange_pref = db.Column(db.Integer) ## or string
    payment_pref = db.Column(db.String)

class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    screen_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/listing')
def listing():
    return render_template('listing.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


if __name__ == '__main__':
    app.run(debug=True)