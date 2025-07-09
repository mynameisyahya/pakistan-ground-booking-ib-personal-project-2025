from flask import Flask, render_template, request, redirect, url_for, flash, session
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
published_grounds = []

@app.route('/')
def home():
    # This function handles the main homepage
    # When someone goes to the website, this is what they see first
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
        password = request.form.get('password')
        if age <= 14:
            return render_template('restriction.html')
        print(f"Player signup: Name={name}, Age={age}, Email={email}, Phone={phone}")
        players[email] = {
            'password': generate_password_hash(password) if password else '',
            'name': name,
            # ...other fields
        }
        session['user_type'] = 'player'
        session['user_email'] = email
        # Redirect to the grounds page after signup
        return redirect(url_for('grounds'))
    # If it's a GET request, show the signup form
    return render_template('signup_player.html')





@app.route('/signup/host', methods=['GET', 'POST'])
def signup_host():
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
        errors = []
        if not all([name, age, email, phone, passwo, ground_name, ground_location, rate, ground_use]):
            errors.append('All fields are required.')
        if not ground_name or not ground_location:
            errors.append('You must list at least one ground name and location.')
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup_host.html')
        if passwo is not None:
            hosts[email] = {
                'password': generate_password_hash(passwo),
                'name': name,
                # ...other fields
            }
        session['user_type'] = 'host'
        session['user_email'] = email
        print(f"Host signup: Name={name}, Age={age}, Email={email}, Phone={phone}, Ground Name={ground_name}, Location={ground_location}, Rate={rate}, Materials={materials}, Use={ground_use}")
        flash('Host account created successfully! (Simulated)', 'success')
        return redirect(url_for('grounds'))
    return render_template('signup_host.html')




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/player', methods=['GET', 'POST'])
def login_player():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = players.get(email)
        if user and ('password' not in user or check_password_hash(user['password'], password)):
            # Login successful!
            session['user_type'] = 'player'
            session['user_email'] = email
            return redirect(url_for('grounds'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login_player.html')
    return render_template('login_player.html')

@app.route('/login/host', methods=['GET', 'POST'])
def login_host():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = hosts.get(email)
        if user and ('password' not in user or check_password_hash(user['password'], password)):
            # Login successful!
            session['user_type'] = 'host'
            session['user_email'] = email
            return redirect(url_for('grounds'))
        else:
            flash('Invalid email or password', 'danger')
            return render_template('login_host.html')
    return render_template('login_host.html')

@app.route('/dashboard/player')
def dashboard_player():
    # Only allow if logged in as player
    return "Player Home Page"

@app.route('/dashboard/host')
def dashboard_host():
    # Only allow if logged in as host
    return "player Home Page"

@app.route('/player/home')
def player_home():
    # Example static data for MVP
    grounds = [
        {
            'id': 1,
            'name': 'Jinnah Sports Complex',
            'location': 'Islamabad',
            'rate': 2000,
            'img': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80'
        },
        {
            'id': 2,
            'name': 'Karachi United Stadium',
            'location': 'Karachi',
            'rate': 1800,
            'img': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80'
        },
        # Add more grounds as needed
    ]
    return render_template('player_home.html', grounds=grounds)

@app.route('/grounds')
def grounds():
    static_grounds = [
        {
            'id': 1,
            'name': 'Jinnah Sports Complex',
            'location': 'Islamabad',
            'rate': 2000,
            'img': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80'
        },
        {
            'id': 2,
            'name': 'Karachi United Stadium',
            'location': 'Karachi',
            'rate': 1800,
            'img': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80'
        },
        {
            'id': 3,
            'name': 'Lahore Football Arena',
            'location': 'Lahore',
            'rate': 2200,
            'img': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=400&q=80'
        },
        {
            'id': 4,
            'name': 'Model Town Sports Complex',
            'location': 'Lahore',
            'rate': 2100,
            'img': 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80'
        },
        {
            'id': 5,
            'name': 'Punjab Stadium',
            'location': 'Lahore',
            'rate': 2300,
            'img': 'https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=400&q=80'
        }
    ]
    all_grounds = static_grounds + published_grounds
    is_host = session.get('user_type') == 'host'
    return render_template('grounds.html', grounds=all_grounds, is_host=is_host)

@app.route('/ground/<int:ground_id>')
def ground_detail(ground_id):
    # For now, just show a placeholder page
    return f"Ground detail and booking for ground {ground_id}"

@app.route('/publish-ground', methods=['GET', 'POST'])
def publish_ground():
    if request.method == 'POST':
        ground = {
            'id': len(published_grounds) + 4,  # unique id after static grounds
            'name': request.form.get('ground_name'),
            'location': request.form.get('location'),
            'rate': request.form.get('rate'),
            'img': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',  # placeholder image
        }
        published_grounds.append(ground)
        flash('Ground published successfully! (Simulated)', 'success')
        return redirect(url_for('grounds'))
    return render_template('publish_ground.html')

if __name__ == '__main__':
    # This runs our Flask app when we execute this file directly
    app.run(debug=True)
    # debug=True shows detailed error messages during development
    # Never use debug=True in production! 

