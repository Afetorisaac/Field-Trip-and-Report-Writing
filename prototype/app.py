"""
Human-Layer Security Awareness Training Platform
A Flask-based web application for simulating social engineering attacks
and training users to recognize security threats.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATABASE = 'security_training.db'

def get_db():
    """Get database connection."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with required tables."""
    if os.path.exists(DATABASE):
        return
    
    db = get_db()
    cursor = db.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create simulations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            scenario TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium'
        )
    ''')
    
    # Create results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            simulation_id INTEGER NOT NULL,
            user_answer TEXT,
            is_correct INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    ''')
    
    # Insert default admin user
    cursor.execute('''
        INSERT INTO users (username, password, email, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin123', 'admin@example.com', 1))
    
    # Insert sample simulations
    simulations = [
        {
            'title': 'Phishing Email Detection',
            'description': 'Identify whether an email is legitimate or a phishing attempt',
            'scenario': '''
You receive an email from "IT-Support@yourcompany-secure.com" with the subject:
"URGENT: Your account will be suspended in 24 hours"

The email states:
"Dear User,

We have detected suspicious activity on your account. To prevent suspension,
please verify your identity by clicking the link below and entering your
credentials:

http://verify-account-security.com/login

Failure to verify within 24 hours will result in permanent account suspension.

Best regards,
IT Security Team"

What should you do?
''',
            'correct_answer': 'report',
            'difficulty': 'easy'
        },
        {
            'title': 'USB Drive in Parking Lot',
            'description': 'Decide how to handle a found USB drive',
            'scenario': '''
You find a USB drive in the company parking lot labeled "Employee Salaries 2024 - CONFIDENTIAL".

What should you do?
''',
            'correct_answer': 'report',
            'difficulty': 'medium'
        },
        {
            'title': 'Social Engineering Phone Call',
            'description': 'Handle a suspicious phone call requesting information',
            'scenario': '''
You receive a phone call from someone claiming to be from the IT department.
They say they need to verify your employee ID and password to complete a
system upgrade that must be done today.

The caller sounds professional and mentions your manager's name correctly.

What should you do?
''',
            'correct_answer': 'refuse',
            'difficulty': 'medium'
        },
        {
            'title': 'Tailgating at Building Entry',
            'description': 'Respond to someone following you into a secure area',
            'scenario': '''
You're entering the office building with your access badge. A person in
business attire carrying a laptop bag follows closely behind you, saying:

"Thanks for holding the door! I forgot my badge at home."

What should you do?
''',
            'correct_answer': 'challenge',
            'difficulty': 'hard'
        }
    ]
    
    for sim in simulations:
        cursor.execute('''
            INSERT INTO simulations (title, description, scenario, correct_answer, difficulty)
            VALUES (?, ?, ?, ?, ?)
        ''', (sim['title'], sim['description'], sim['scenario'], 
              sim['correct_answer'], sim['difficulty']))
    
    db.commit()
    db.close()
    print("Database initialized successfully!")

# Initialize database on startup
init_db()

@app.route('/')
def landing():
    """Landing page."""
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('register'))
        
        db = get_db()
        cursor = db.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, password, email))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        finally:
            db.close()
    
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                      (username, password))
        user = cursor.fetchone()
        db.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('landing.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('landing'))

@app.route('/dashboard')
def index():
    """User dashboard."""
    if 'user_id' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('landing'))
    
    db = get_db()
    cursor = db.cursor()
    
    # Get user statistics
    cursor.execute('''
        SELECT COUNT(*) as total, SUM(is_correct) as correct
        FROM results
        WHERE user_id = ?
    ''', (session['user_id'],))
    stats = cursor.fetchone()
    
    # Get available simulations
    cursor.execute('SELECT * FROM simulations')
    simulations = cursor.fetchall()
    
    db.close()
    
    return render_template('index.html', 
                         stats=stats,
                         simulations=simulations)

@app.route('/simulate/<int:sim_id>', methods=['GET', 'POST'])
def simulate(sim_id):
    """Run a simulation."""
    if 'user_id' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('landing'))
    
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        # Get simulation details
        cursor.execute('SELECT * FROM simulations WHERE id = ?', (sim_id,))
        simulation = cursor.fetchone()
        
        if not simulation:
            flash('Simulation not found', 'error')
            return redirect(url_for('index'))
        
        # Check if answer is correct
        is_correct = 1 if user_answer == simulation['correct_answer'] else 0
        
        # Store result
        cursor.execute('''
            INSERT INTO results (user_id, simulation_id, user_answer, is_correct)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], sim_id, user_answer, is_correct))
        db.commit()
        
        # Prepare feedback
        feedback = {
            'correct': is_correct,
            'answer': user_answer,
            'correct_answer': simulation['correct_answer'],
            'explanation': get_explanation(simulation['correct_answer'])
        }
        
        db.close()
        return render_template('simulate.html', 
                             simulation=simulation, 
                             feedback=feedback,
                             completed=True)
    
    # GET request - show simulation
    cursor.execute('SELECT * FROM simulations WHERE id = ?', (sim_id,))
    simulation = cursor.fetchone()
    db.close()
    
    if not simulation:
        flash('Simulation not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('simulate.html', simulation=simulation, completed=False)

@app.route('/admin')
def admin():
    """Admin dashboard."""
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cursor = db.cursor()
    
    # Get all users and their statistics
    cursor.execute('''
        SELECT u.id, u.username, u.email, u.created_at,
               COUNT(r.id) as total_attempts,
               SUM(r.is_correct) as correct_attempts
        FROM users u
        LEFT JOIN results r ON u.id = r.user_id
        WHERE u.is_admin = 0
        GROUP BY u.id
    ''')
    users = cursor.fetchall()
    
    # Get overall statistics
    cursor.execute('''
        SELECT COUNT(DISTINCT user_id) as total_users,
               COUNT(*) as total_attempts,
               SUM(is_correct) as correct_attempts
        FROM results
    ''')
    overall = cursor.fetchone()
    
    # Get recent activity
    cursor.execute('''
        SELECT u.username, s.title, r.is_correct, r.completed_at
        FROM results r
        JOIN users u ON r.user_id = u.id
        JOIN simulations s ON r.simulation_id = s.id
        ORDER BY r.completed_at DESC
        LIMIT 10
    ''')
    recent = cursor.fetchall()
    
    db.close()
    
    return render_template('admin.html', 
                         users=users, 
                         overall=overall,
                         recent=recent)

def get_explanation(correct_answer):
    """Get explanation for the correct answer."""
    explanations = {
        'report': 'You should report this to your security team immediately. Never click suspicious links or provide credentials based on urgent requests.',
        'refuse': 'Never provide credentials over the phone. Legitimate IT staff will never ask for your password. Always verify through official channels.',
        'challenge': 'Even if someone looks professional, always ensure they have proper access credentials. Politely ask them to use their own badge or contact security.',
        'ignore': 'This is suspicious and should be reported to security. Do not interact with unknown media or devices.',
        'verify': 'Always verify unexpected requests through official channels before taking action.'
    }
    return explanations.get(correct_answer, 'Always verify suspicious activity with your security team.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
