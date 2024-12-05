from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialises the app for Flask
app = Flask(__name__)
# Generates the flask secret key
app.secret_key = 'This is my secret key!'
# Configures the SQL database and stores it as 'site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Creates the database using the flask app
db = SQLAlchemy(app)

# Creates a table in the database to store user logins
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Redirects the user away from the root
@app.route('/', methods=['GET', 'POST'])
def root():
    return redirect(url_for('index'))

# Generates the route for the home page
@app.route('/home')
def index():
    return render_template('index.html')

# Generates the route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['password_confirm']
        if password != confirm_password:
            flash('Passwords do not match', 'failure')
            return redirect(url_for('register'))
        elif password == confirm_password:
            if username not in User.query.filter_by(username=username):
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000')
                new_user = User(username=username, password=hashed_password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Account created, please login', 'success')
                except:
                    flash('An error occurred while adding the new user', 'failure')
    return render_template('register.html')

# Generates the route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# Generates the route for the logout page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('index'))

# Generates the route for the workouts page
@app.route('/workouts')
def workouts():
    return render_template('workouts.html')

# Generates the route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Generates the route for the diets page
@app.route('/diets')
def diets():
    return render_template('diets.html')

# Generates the route for the PT Booking page
@app.route('/PT-book', methods=['GET', 'POST'])
def PTbook():
    return render_template('PTbook.html')

# Runs the code in debug mode. Also generates anything to do with the database such as tables and data.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
