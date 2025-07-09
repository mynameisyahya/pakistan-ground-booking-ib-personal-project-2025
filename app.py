from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import random
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
        # requirements for an account
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']  # Now required field
        
        # Validate required fields
        if not all([name, email, phone, password]):
            flash('All fields are required.', 'danger')
            return render_template('signup_player.html')
            
        if age <= 14:
            return render_template('restriction.html')
            
        # Check if email already exists
        if email in players:
            flash('Email already registered. Please login or use a different email.', 'danger')
            return render_template('signup_player.html')
            
        print(f"Player signup: Name={name}, Age={age}, Email={email}, Phone={phone}")
        players[email] = {
            'password': generate_password_hash(password),
            'name': name,
            'age': age,
            'email': email,
            'phone': phone
        }
        session['user_type'] = 'player'
        session['user_email'] = email
        flash('Account created successfully! Welcome!', 'success')
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
        password = request.form.get('password')
        ground_name = request.form.get('ground_name')
        ground_location = request.form.get('ground_location')
        rate = request.form.get('rate')
        materials = request.form.getlist('materials')
        ground_use = request.form.get('ground_use')
        
        # Validate required fields
        if not all([name, age, email, phone, password, ground_name, ground_location, rate, ground_use]):
            flash('All fields are required.', 'danger')
            return render_template('signup_host.html')
            
        # Ensure password is not None for type safety
        if not password:
            flash('Password is required.', 'danger')
            return render_template('signup_host.html')
            
        # Check if email already exists
        if email in hosts:
            flash('Email already registered. Please login or use a different email.', 'danger')
            return render_template('signup_host.html')
            
        hosts[email] = {
            'password': generate_password_hash(password),
            'name': name,
            'age': age,
            'email': email,
            'phone': phone,
            'ground_name': ground_name,
            'ground_location': ground_location,
            'rate': rate,
            'materials': materials,
            'ground_use': ground_use
        }
        session['user_type'] = 'host'
        session['user_email'] = email
        # List of random Unsplash images
        unsplash_images = [
            'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1518098268026-4e89f1a2cd8e?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1465378552210-88481e0b7c33?auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1505843273132-bc5c6f7bfa98?auto=format&fit=crop&w=400&q=80',
        ]
        random_img = random.choice(unsplash_images)
        host_ground = {
            'name': ground_name,
            'location': ground_location,
            'rate': rate,
            'img': random_img,
        }
        print(f"Host signup: Name={name}, Age={age}, Email={email}, Phone={phone}, Ground Name={ground_name}, Location={ground_location}, Rate={rate}, Materials={materials}, Use={ground_use}")
        flash('Host account created successfully! Welcome!', 'success')
        # Redirect to the host-specific grounds page, passing the host's ground
        return redirect(url_for('grounds_host', host_ground_name=ground_name, host_ground_location=ground_location, host_ground_rate=rate, host_ground_img=random_img))
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
        
        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            # Login successful!
            session['user_type'] = 'player'
            session['user_email'] = email
            flash('Login successful!', 'success')
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
        
        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            # Login successful!
            session['user_type'] = 'host'
            session['user_email'] = email
            flash('Login successful!', 'success')
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

@app.route('/grounds/host')
def grounds_host():
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
    # Get host ground from query params if present
    host_ground = None
    host_ground_name = request.args.get('host_ground_name')
    host_ground_location = request.args.get('host_ground_location')
    host_ground_rate = request.args.get('host_ground_rate')
    host_ground_img = request.args.get('host_ground_img')
    if host_ground_name and host_ground_location and host_ground_rate:
        host_ground = {
            'name': host_ground_name,
            'location': host_ground_location,
            'rate': host_ground_rate,
            'img': host_ground_img or 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
        }
        # Remove from all_grounds if present
        all_grounds = [g for g in all_grounds if not (g['name'] == host_ground_name and g['location'] == host_ground_location)]
    return render_template('grounds_host.html', grounds=all_grounds, host_ground=host_ground)

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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # This runs our Flask app when we execute this file directly
    app.run(debug=True)
    # debug=True shows detailed error messages during development
    # Never use debug=True in production! 

