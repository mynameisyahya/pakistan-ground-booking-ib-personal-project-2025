from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_sqlalchemy import SQLAlchemy
import os
from markupsafe import escape
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

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grounds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Ground model
class Ground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(300), nullable=False)
    published = db.Column(db.Boolean, default=False)
    host_email = db.Column(db.String(120), nullable=False)
    materials = db.Column(db.String(300), nullable=True)  # Comma-separated list
    ground_use = db.Column(db.String(50), nullable=True)

# Create the database and tables if they don't exist
if not os.path.exists('grounds.db'):
    with app.app_context():
        db.create_all()

# One-time migration: insert static grounds if DB is empty
with app.app_context():
    if Ground.query.count() == 0:
        static_grounds = [
            Ground(
                name='Jinnah Sports Complex',
                location='Islamabad',
                rate=2000,
                img='https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
                published=True,
                host_email='demo@host.com',
                materials='Football,Goal Post',
                ground_use='Football'
            ),
            Ground(
                name='Karachi United Stadium',
                location='Karachi',
                rate=1800,
                img='https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
                published=True,
                host_email='demo@host.com',
                materials='Football,Goal Post',
                ground_use='Football'
            ),
            Ground(
                name='Lahore Football Arena',
                location='Lahore',
                rate=2200,
                img='https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=400&q=80',
                published=True,
                host_email='demo@host.com',
                materials='Football,Goal Post',
                ground_use='Football'
            ),
            Ground(
                name='Model Town Sports Complex',
                location='Lahore',
                rate=2100,
                img='https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80',
                published=True,
                host_email='demo@host.com',
                materials='Football,Goal Post',
                ground_use='Football'
            ),
            Ground(
                name='Punjab Stadium',
                location='Lahore',
                rate=2300,
                img='https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=400&q=80',
                published=True,
                host_email='demo@host.com',
                materials='Football,Goal Post',
                ground_use='Football'
            ),
        ]
        db.session.bulk_save_objects(static_grounds)
        db.session.commit()

# Example user stores
players = {}
hosts = {}

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
        try:
            # requirements for an account
            name = escape(request.form['name'].strip())
            age = int(request.form['age'])
            email = escape(request.form['email'].strip())
            phone = escape(request.form['phone'].strip())
            password = request.form['password']  # Now required field
            
            # Validate required fields
            if not all([name, email, phone, password]):
                flash('All fields are required.', 'danger')
                return render_template('signup_player.html')
                
            # Validate age
            if age <= 14:
                return render_template('restriction.html')
            if age > 120:  # Reasonable upper limit
                flash('Please enter a valid age.', 'danger')
                return render_template('signup_player.html')
                
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
            
        except ValueError:
            flash('Please enter a valid age (numbers only).', 'danger')
            return render_template('signup_player.html')
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return render_template('signup_player.html')
        except Exception as e:
            flash('An error occurred during signup. Please try again.', 'danger')
            print(f"Player signup error: {e}")
            return render_template('signup_player.html')
            
    # If it's a GET request, show the signup form
    return render_template('signup_player.html')





@app.route('/signup/host', methods=['GET', 'POST'])
def signup_host():
    if request.method == 'POST':
        try:
            name = escape(request.form.get('name', '').strip())
            age = request.form.get('age')
            email = escape(request.form.get('email', '').strip())
            phone = escape(request.form.get('phone', '').strip())
            password = request.form.get('password')
            ground_name = escape(request.form.get('ground_name', '').strip())
            ground_location = escape(request.form.get('ground_location', '').strip())
            rate = request.form.get('rate')
            materials = [escape(m.strip()) for m in request.form.getlist('materials')]
            ground_use = escape(request.form.get('ground_use', '').strip())

            # Validate required fields
            if not all([name, age, email, phone, password, ground_name, ground_location, rate, ground_use]):
                flash('All fields are required.', 'danger')
                return render_template('signup_host.html')
            if not password:
                flash('Password is required.', 'danger')
                return render_template('signup_host.html')
            try:
                if age is None or age == '':
                    raise ValueError('Age is required')
                age_int = int(age)
                if age_int <= 14:
                    flash('You must be at least 15 years old to register as a host.', 'danger')
                    return render_template('signup_host.html')
                if age_int > 120:
                    flash('Please enter a valid age.', 'danger')
                    return render_template('signup_host.html')
            except ValueError:
                flash('Please enter a valid age (numbers only).', 'danger')
                return render_template('signup_host.html')
            try:
                if rate is None or rate == '':
                    raise ValueError('Rate is required')
                rate_int = int(rate)
                if rate_int < 0:
                    flash('Rate must be a positive number.', 'danger')
                    return render_template('signup_host.html')
            except ValueError:
                flash('Please enter a valid rate (numbers only).', 'danger')
                return render_template('signup_host.html')
            # Check if host already exists by email in grounds table (host_email)
            existing_ground = Ground.query.filter_by(host_email=email).first()
            if existing_ground:
                flash('Email already registered as a host. Please login or use a different email.', 'danger')
                return render_template('signup_host.html')
            session['user_type'] = 'host'
            session['user_email'] = email
            # Add the ground to the database as unpublished
            img = 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80'
            new_ground = Ground(
                name=ground_name,
                location=ground_location,
                rate=rate_int,
                img=img,
                published=False,
                host_email=email,
                materials=','.join(materials),
                ground_use=ground_use
            )
            db.session.add(new_ground)
            db.session.commit()
            flash('Host account created! Preview your ground before publishing.', 'success')
            return redirect(url_for('grounds_host'))
        except Exception as e:
            flash('An error occurred during signup. Please try again.', 'danger')
            print(f"Host signup error: {e}")
            return render_template('signup_host.html')
    return render_template('signup_host.html')

@app.route('/publish-ground/<int:ground_id>', methods=['POST'])
def publish_ground_action(ground_id):
    # Only the host who owns the ground can publish it
    if 'user_email' not in session or session.get('user_type') != 'host':
        flash('You must be logged in as a host to publish a ground.', 'danger')
        return redirect(url_for('login_host'))
    ground = Ground.query.get_or_404(ground_id)
    if ground.host_email != session['user_email']:
        flash('You do not have permission to publish this ground.', 'danger')
        return redirect(url_for('grounds_host'))
    ground.published = True
    db.session.commit()
    flash('Ground published successfully!', 'success')
    return redirect(url_for('grounds_host'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/player', methods=['GET', 'POST'])
def login_player():
    if request.method == 'POST':
        try:
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
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return render_template('login_player.html')
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            print(f"Player login error: {e}")
            return render_template('login_player.html')
    return render_template('login_player.html')

@app.route('/login/host', methods=['GET', 'POST'])
def login_host():
    if request.method == 'POST':
        try:
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
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return render_template('login_host.html')
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            print(f"Host login error: {e}")
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
    # Show only published grounds to all users
    grounds = Ground.query.filter_by(published=True).all()
    is_host = session.get('user_type') == 'host'
    return render_template('grounds.html', grounds=grounds, is_host=is_host)

@app.route('/grounds/host')
def grounds_host():
    # Show all grounds for the logged-in host (published and unpublished)
    if 'user_email' not in session or session.get('user_type') != 'host':
        flash('You must be logged in as a host to view this page.', 'danger')
        return redirect(url_for('login_host'))
    host_email = session['user_email']
    # All grounds for this host
    host_grounds = Ground.query.filter_by(host_email=host_email).all()
    # Unpublished ground for preview (if any)
    host_ground = next((g for g in host_grounds if not g.published), None)
    # Only show published grounds in the main list
    published_grounds = [g for g in host_grounds if g.published]
    return render_template('grounds_host.html', grounds=published_grounds, host_ground=host_ground)

@app.route('/ground/<int:ground_id>')
def ground_detail(ground_id):
    # For now, just show a placeholder page
    return f"Ground detail and booking for ground {ground_id}"

@app.route('/publish-ground', methods=['GET', 'POST'])
def publish_ground():
    if request.method == 'POST':
        # Add new ground to the database (unpublished by default)
        name = escape(request.form.get('ground_name', '').strip())
        location = escape(request.form.get('location', '').strip())
        rate = request.form.get('rate')
        img = 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80'  # placeholder image
        host_email = escape(session.get('user_email', 'demo@host.com').strip())
        materials = escape(request.form.get('materials', '').strip())
        ground_use = escape(request.form.get('ground_use', '').strip())
        new_ground = Ground(
            name=name,
            location=location,
            rate=int(rate) if rate else 0,
            img=img,
            published=False,  # Not published until host confirms
            host_email=host_email,
            materials=materials,
            ground_use=ground_use
        )
        db.session.add(new_ground)
        db.session.commit()
        flash('Ground created! Preview it before publishing.', 'success')
        return redirect(url_for('grounds_host'))
    return render_template('publish_ground.html')

@app.route('/final-booking/<int:ground_id>', methods=['GET', 'POST'])
def final_booking(ground_id):
    ground = Ground.query.get_or_404(ground_id)
    if request.method == 'POST':
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        player_email = session.get('user_email')
        if not player_email:
            flash('You must be logged in as a player to book.', 'danger')
            return redirect(url_for('login_player'))
        # Create booking request
        booking = Booking(
            ground_id=ground.id,
            player_email=player_email,
            date=date,
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking request sent to the host!', 'success')
        return redirect(url_for('player_dashboard'))
    return render_template('final_booking.html', ground=ground)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ground_id = db.Column(db.Integer, db.ForeignKey('ground.id'), nullable=False)
    player_email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, declined

# Ensure all tables are created automatically
with app.app_context():
    db.create_all()

@app.route('/host/dashboard', methods=['GET', 'POST'])
def host_dashboard():
    if 'user_email' not in session or session.get('user_type') != 'host':
        flash('You must be logged in as a host to view this page.', 'danger')
        return redirect(url_for('login_host'))
    host_email = session['user_email']
    # Get all grounds owned by this host
    host_grounds = Ground.query.filter_by(host_email=host_email).all()
    ground_ids = [g.id for g in host_grounds]
    # Get all bookings for these grounds
    bookings = Booking.query.filter(Booking.ground_id.in_(ground_ids)).order_by(Booking.id.desc()).all()
    # Notification: count of pending requests
    pending_count = sum(1 for b in bookings if b.status == 'pending')
    return render_template('host_dashboard.html', bookings=bookings, host_grounds=host_grounds, pending_count=pending_count)

@app.route('/booking/<int:booking_id>/approve', methods=['POST'])
def approve_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    # Only the host of the ground can approve
    ground = Ground.query.get(booking.ground_id)
    if session.get('user_email') != ground.host_email:
        flash('You do not have permission to approve this booking.', 'danger')
        return redirect(url_for('host_dashboard'))
    booking.status = 'approved'
    db.session.commit()
    flash('Booking approved.', 'success')
    return redirect(url_for('host_dashboard'))

@app.route('/booking/<int:booking_id>/decline', methods=['POST'])
def decline_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    ground = Ground.query.get(booking.ground_id)
    if session.get('user_email') != ground.host_email:
        flash('You do not have permission to decline this booking.', 'danger')
        return redirect(url_for('host_dashboard'))
    booking.status = 'declined'
    db.session.commit()
    flash('Booking declined.', 'success')
    return redirect(url_for('host_dashboard'))

@app.route('/player/dashboard')
def player_dashboard():
    if 'user_email' not in session or session.get('user_type') != 'player':
        flash('You must be logged in as a player to view this page.', 'danger')
        return redirect(url_for('login_player'))
    player_email = session['user_email']
    bookings = Booking.query.filter_by(player_email=player_email).order_by(Booking.id.desc()).all()
    # Get all grounds for display
    ground_ids = [b.ground_id for b in bookings]
    grounds = {g.id: g for g in Ground.query.filter(Ground.id.in_(ground_ids)).all()}
    return render_template('player_dashboard.html', bookings=bookings, grounds=grounds)

if __name__ == '__main__':
    # This runs our Flask app when we execute this file directly
    app.run(debug=True)
    # debug=True shows detailed error messages during development
    # Never use debug=True in production! 

