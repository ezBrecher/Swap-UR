from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
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
    item_category=db.Column(db.String(255))
    img_1_name = db.Column(db.String(255))
    img_1_path = db.Column(db.String(255))
    # img_2 = db.Column(db.String(255))
    # img_3 = db.Column(db.String(255))
    # img_4 = db.Column(db.String(255))
    # img_5 = db.Column(db.String(255))
    price = db.Column(db.Float(2), nullable=False)
    condition = db.Column(db.String(50))
    listing_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    sold = db.Column(db.Boolean)
    exchange_pref = db.Column(db.Integer) ## or string
    payment_pref = db.Column(db.String)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/item')
def item():
    #pass item somehow
    return render_template('item1.html', item=item)

@app.route('/listing', methods=["POST","GET"])
def listing():
    if request.method == "POST":
        input = request.form
        im1 = request.files['img_1']
        im1_name = secure_filename(im1.filename)
        im1_path = os.path.join(app.config['UPLOAD_FOLDER'], im1_name)
        im1.save(im1_path)
        new_item = Item(name=input["name"],
                        description=input["description"],
                        item_category=input["item_category"],
                        img_1_name=im1_name,
                        img_1_path=im1_path,
                        # img_2=input["img_2"],
                        # img_3=input["img_3"],
                        # img_4=input["img_4"],
                        # img_5=input["img_5"],
                        price=input["price"],
                        condition=input["condition"])
        db.session.add(new_item)
        db.session.commit()
        flash("successfully added item")
        return redirect(url_for("item"))
    else:
        return render_template('listing.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user is not None:
            session['user_id'] = user.u_id
            return redirect(url_for('main'))
        else:
            error_message = "Invalid email or password"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
