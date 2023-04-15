from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length
# from flask_wtf import FlaskForm
from flask import Flask, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

## database declarations
class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    screen_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer)

class Item(db.Model):
    i_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    seller = db.Column(db.Integer, nullable = False)
    category_1 = db.Column(db.String(50), nullable=False)
    category_2 = db.Column(db.String(50))
    category_3 = db.Column(db.String(50))
    img_1 = db.Column(db.LargeBinary)
    img_2 = db.Column(db.LargeBinary)
    img_3 = db.Column(db.LargeBinary)
    img_4 = db.Column(db.LargeBinary)
    img_5 = db.Column(db.LargeBinary)
    price = db.Column(db.Float(2), nullable=False)
    condition = db.Column(db.String(50))
    listing_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    sold = db.Column(db.Boolean)
    exchange_pref = db.Column(db.Integer) ## or string
    payment_pref = db.Column(db.String)

# db.ForeignKey('User.u_id'),



# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/item')
def item():
    return render_template('item.html')

@app.route('/listing',methods=['POST'])
def listing():
    img1 = request.files['img_1']
    img2 = request.files['img_2']
    img3 = request.files['img_3']
    img4 = request.files['img_4']
    img5 = request.files['img_5']
    new_item = Item(img_1=img1,
                    img_2=img2,
                    img_3=img3,
                    img_4=img4,
                    img_5=img5)
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

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
