from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length
# from flask_wtf import FlaskForm
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    item_category = db.Column(db.String(50), nullable=False)
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

@app.route('/listing', methods=["POST","GET"])
def listing():
    if request.method == "POST":
        input = request.form
        new_item = Item(name=input["name"],
                        description=input["description"],
                        item_category=input["item_category"],
                        img_1=input["img_1"],
                        img_2=input["img_2"],
                        img_3=input["img_3"],
                        img_4=input["img_4"],
                        img_5=input["img_5"],
                        price=input["price"],
                        condition=input["condition"])
        db.add(new_item)
        db.commit()
        flash("successfully added item")
        return redirect(url_for("item"))
    else:
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
