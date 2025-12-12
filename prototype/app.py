"""
Minimal Flask Prototype for Phishing Simulation Platform Demo
This is a demonstration prototype showing basic functionality
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database setup
DATABASE = 'phishing_demo.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            template TEXT NOT NULL,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Campaign interactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            user_email TEXT,
            action_type TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')
    
    # Training courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add sample data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ('admin@example.com', 'Admin User', 'admin'),
            ('john.doe@example.com', 'John Doe', 'user'),
            ('jane.smith@example.com', 'Jane Smith', 'user')
        ]
        cursor.executemany('INSERT INTO users (email, name, role) VALUES (?, ?, ?)', sample_users)
        
        sample_courses = [
            ('Introduction to Phishing', 'Learn the basics of phishing attacks and how to identify them'),
            ('Advanced Email Security', 'Deep dive into email security best practices'),
            ('Social Engineering Awareness', 'Understanding social engineering tactics')
        ]
        cursor.executemany('INSERT INTO courses (title, description) VALUES (?, ?)', sample_courses)
    
    conn.commit()
    conn.close()

# Initialize database on startup
with app.app_context():
    init_db()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Admin dashboard"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM interactions WHERE action_type='click'")
    click_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC LIMIT 5")
    recent_campaigns = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'users': user_count,
        'campaigns': campaign_count,
        'clicks': click_count
    }
    
    return render_template('admin.html', stats=stats, campaigns=recent_campaigns)

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    """Phishing simulation page"""
    if request.method == 'POST':
        campaign_name = request.form.get('campaign_name')
        template = request.form.get('template')
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO campaigns (name, template, status) VALUES (?, ?, ?)',
                      (campaign_name, template, 'active'))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin'))
    
    return render_template('simulate.html')

@app.route('/landing/<int:campaign_id>')
def landing(campaign_id):
    """Landing page shown after clicking simulated phishing link"""
    user_email = request.args.get('email', 'unknown@example.com')
    
    # Log the interaction
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO interactions (campaign_id, user_email, action_type) VALUES (?, ?, ?)',
                  (campaign_id, user_email, 'click'))
    conn.commit()
    conn.close()
    
    return render_template('landing.html', campaign_id=campaign_id)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.name, COUNT(i.id) as clicks
        FROM campaigns c
        LEFT JOIN interactions i ON c.id = i.campaign_id
        WHERE i.action_type = 'click'
        GROUP BY c.id, c.name
        ORDER BY clicks DESC
        LIMIT 5
    """)
    
    campaign_stats = [{'name': row[0], 'clicks': row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'campaign_performance': campaign_stats
    })

@app.route('/courses')
def courses():
    """Training courses listing"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'courses': [{'id': c[0], 'title': c[1], 'description': c[2]} for c in courses]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
