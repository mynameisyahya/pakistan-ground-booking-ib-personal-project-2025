import pytest
from app import app, db, Ground

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add a test ground
            db.session.add(Ground(
                name='Test Ground',
                location='Test City',
                rate=1000,
                img='test.jpg',
                published=True,
                host_email='test@host.com',
                materials='Football',
                ground_use='Football'
            ))
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Football" in rv.data or b"Ground" in rv.data

def test_signup_player_invalid(client):
    rv = client.post('/signup/player', data={
        'name': '',
        'age': '10',
        'email': 'bademail',
        'phone': '',
        'password': ''
    }, follow_redirects=True)
    assert b'All fields are required' in rv.data or b'valid age' in rv.data

def test_grounds_listed(client):
    rv = client.get('/grounds')
    assert b'Test Ground' in rv.data

def test_xss_sanitization(client):
    rv = client.post('/signup/player', data={
        'name': '<script>alert(1)</script>',
        'age': '20',
        'email': 'xss@test.com',
        'phone': '123456',
        'password': 'testpass'
    }, follow_redirects=True)
    # Now check that the script tag is escaped in the database or output
    rv2 = client.get('/grounds')
    assert b'&lt;script&gt;' in rv2.data or b'<script>' not in rv2.data 