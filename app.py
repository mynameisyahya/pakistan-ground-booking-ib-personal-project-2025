from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
# render_template: Used to display HTML pages
# request: Handles data sent from forms
# redirect: Sends users to different pages
# url_for: Creates URLs for our routes
# flash: Shows temporary messages to users

app = Flask(__name__)
# Create a Flask application instance
# __name__ tells Flask where to look for templates and static files

app.secret_key = 'PASSWORD'
# Secret key is needed for flash messages and session management
# In production, you'd use a more secure random key

# Example user stores
players = {}
hosts = {}

@app.route('/')
def home():
    # This function handles the main homepage
    # When someone visits our website, this is what they see first
    return render_template('index.html')
    # render_template looks for a file called 'index.html' in the templates folder




@app.route('/signup/player', methods=['GET', 'POST'])
def signup_player():
    # This route handles both GET (show form) and POST (process form) requests
    if request.method == 'POST':
        # requirments for an account
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']
        phone = request.form['phone']
        if age <= 14:
            return render_template('restriction.html')
        print(f"Player signup: Name={name}, Age={age}, Email={email}, Phone={phone}")
        players[email] = {
            'name': name,
            # ...other fields
        }
        # Redirect to the grounds page after signup
        return redirect(url_for('grounds'))
    # If it's a GET request, show the signup form
    return render_template('signup_player.html')





@app.route('/signup/landlord', methods=['GET', 'POST'])
def signup_landlord():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')
        phone = request.form.get('phone')
        passwo = request.form.get('password')
        ground_name = request.form.get('ground_name')
        ground_location = request.form.get('ground_location')
        rate = request.form.get('rate')
        materials = request.form.getlist('materials')
        ground_use = request.form.get('ground_use')
        # requirments for an account
        errors = []
        if not all([name, age, email, phone, ground_name, ground_location, rate, ground_use]):
            errors.append('All fields are required.')
        if not ground_name or not ground_location:
            errors.append('You must list at least one ground name and location.')
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup_landlord.html')
        # if these things are not written it will error out
        print(f"Landlord signup: Name={name}, Age={age}, Email={email}, Phone={phone}, Ground Name={ground_name}, Location={ground_location}, Rate={rate}, Materials={materials}, Use={ground_use}")
        if passwo == None:
            return render_template('restriction.html')
        
        hosts[email] = {
            'password': generate_password_hash(passwo),
            'name': name,
            # ...other fields
        }
        flash('Landlord account created successfully! (Simulated)', 'success')
        return redirect(url_for('grounds'))
    
    return render_template('signup_landlord.html')




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/player', methods=['GET', 'POST'])
def login_player():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # For player login
        user = players.get(email)
        if user and check_password_hash(user['password'], password):
            # Login successful!
            # Set session, redirect, etc.
            return redirect(url_for('dashboard_player'))
        else:
            # Invalid credentials
            flash('Invalid email or password', 'danger')
            return render_template('login_player.html')
    return render_template('login_player.html')

@app.route('/login/host', methods=['GET', 'POST'])
def login_host():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
      
    return render_template('login_host.html')

@app.route('/dashboard/player')
def dashboard_player():
    # Only allow if logged in as player
    return "Player Home Page"

@app.route('/dashboard/host')
def dashboard_host():
    # Only allow if logged in as host
    return "Host Home Page"

@app.route('/grounds')
def grounds():
    return "Grounds page coming soon!"

if __name__ == '__main__':
    # This runs our Flask app when we execute this file directly
    app.run(debug=True)
    # debug=True shows detailed error messages during development
    # Never use debug=True in production! 

