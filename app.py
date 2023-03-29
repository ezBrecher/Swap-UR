from flask import Flask, render_template

app = Flask(__name__)

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