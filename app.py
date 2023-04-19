from flask import Flask, render_template, request, redirect, session, url_for, flash
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
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    seller = db.Column(db.Integer)
    item_category = db.Column(db.String(255))
    img_1_name = db.Column(db.String(255))
    img_1_path = db.Column(db.String(255))
    img_2_name = db.Column(db.String(255))
    img_2_path = db.Column(db.String(255))
    img_3_name = db.Column(db.String(255))
    img_3_path = db.Column(db.String(255))
    img_4_name = db.Column(db.String(255))
    img_4_path = db.Column(db.String(255))
    img_5_name = db.Column(db.String(255))
    img_5_path = db.Column(db.String(255))
    price = db.Column(db.Float(2), default=0)
    condition = db.Column(db.String(50))
    listing_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    sold = db.Column(db.Boolean)
    exchange_pref = db.Column(db.Integer) ## or string

@app.route('/')
def main():
    category = request.args.get('category', '')
    condition = request.args.get('condition', '')
    price_range = request.args.get('price', '')
    items = Item.query.all()

    if category:
        items = [item for item in items if item.item_category == category]
    if condition:
        items = [item for item in items if item.condition == condition]
    if price_range:
        prices = price_range.split('-')
        if len(prices) == 2:
            min_price, max_price = float(prices[0]), float(prices[1])
            items = [item for item in items if min_price <= item.price <= max_price]

    return render_template('main.html', items=items)

@app.route('/item')
def item():
    #pass item somehow
    return render_template('item1.html', item=item)

@app.route('/listing', methods=['POST','GET'])
def listing():
    if request.method == 'POST':
        input = request.form

        im1_name = None
        im2_name = None
        im3_name = None
        im4_name = None
        im5_name = None

        im1_path = None
        im2_path = None
        im3_path = None
        im4_path = None
        im5_path = None

        im1 = request.files['img_1']
        im1.seek(0, os.SEEK_END)
        if im1.tell() != 0:
            im1_name = secure_filename(im1.filename)
            im1_path = os.path.join(app.config['UPLOAD_FOLDER'], im1_name)
            im1.save(im1_path)

        im2 = request.files['img_2']
        im2.seek(0, os.SEEK_END)
        if im2.tell() != 0:
            im2_name = secure_filename(im2.filename)
            im2_path = os.path.join(app.config['UPLOAD_FOLDER'], im2_name)
            im2.save(im2_path)

        im3 = request.files['img_3']
        im3.seek(0, os.SEEK_END)
        if im3.tell() != 0:
            im3_name = secure_filename(im3.filename)
            im3_path = os.path.join(app.config['UPLOAD_FOLDER'], im3_name)
            im3.save(im3_path)

        im4 = request.files['img_4']
        im4.seek(0, os.SEEK_END)
        if im4.tell() != 0:
            im4_name = secure_filename(im4.filename)
            im4_path = os.path.join(app.config['UPLOAD_FOLDER'], im4_name)
            im4.save(im4_path)

        im5 = request.files['img_5']
        im5.seek(0, os.SEEK_END)
        if im5.tell() != 0:
            im5_name = secure_filename(im5.filename)
            im5_path = os.path.join(app.config['UPLOAD_FOLDER'], im5_name)
            im5.save(im5_path)

        new_item = Item(name=input["name"],
                        description=input["description"],
                        item_category=input["item_category"],
                        img_1_name=im1_name,
                        img_1_path=im1_path,
                        img_2_name=im2_name,
                        img_2_path=im2_path,
                        img_3_name=im3_name,
                        img_3_path=im3_path,
                        img_4_name=im4_name,
                        img_4_path=im4_path,
                        img_5_name=im5_name,
                        img_5_path=im5_path,
                        price=input["price"],
                        condition=input["condition"],
                        sold=False)
        db.session.add(new_item)
        db.session.commit()
        flash("successfully added item")
        return redirect(url_for("item") )
    else:
        return render_template('listing.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/confirmation')
def confirmation():
    id = 2
    item = Item.query.filter_by(i_id=id).first()
    if item:
        if item.sold == True:
            return render_template('confirmation.html', item=item)
        else:
            flash("item hasn't been sold yet")
            return render_template('item.html', item=item)
    else:
        return 'Item not found'

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
