from flask import Flask, render_template, request, redirect, url_for, flash
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
        # Redirect to the home page after signup
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
        ground_name = request.form.get('ground_name')
        ground_location = request.form.get('ground_location')
        rate = request.form.get('rate')
        materials = request.form.getlist('materials')
        ground_use = request.form.get('ground_use')
        # Validation: all fields required, at least one ground location
        errors = []
        if not all([name, age, email, phone, ground_name, ground_location, rate, ground_use]):
            errors.append('All fields are required.')
        if not ground_name or not ground_location:
            errors.append('You must list at least one ground name and location.')
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup_landlord.html')
        # For now, just print the data (simulate saving to DB)
        print(f"Landlord signup: Name={name}, Age={age}, Email={email}, Phone={phone}, Ground Name={ground_name}, Location={ground_location}, Rate={rate}, Materials={materials}, Use={ground_use}")
        flash('Landlord account created successfully! (Simulated)', 'success')
        return redirect(url_for('grounds'))
    return render_template('signup_landlord.html')

@app.route('/login')
def login():
    # This will handle user login
    # We'll create this later
    return "Login Page - Coming Soon!"

@app.route('/grounds')
def grounds():
    return "Grounds page coming soon!"

if __name__ == '__main__':
    # This runs our Flask app when we execute this file directly
    app.run(debug=True)
    # debug=True shows detailed error messages during development
    # Never use debug=True in production! 

