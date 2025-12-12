"""
SOC-Lite Prototype
A minimal Security Operations Center demonstration system for log ingestion and alerting.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-soc-key')

DATABASE = 'soc.db'

def get_db():
    """Get database connection."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize the database with required tables."""
    db = get_db()
    cursor = db.cursor()
    
    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT NOT NULL,
            severity TEXT NOT NULL,
            event_type TEXT,
            message TEXT NOT NULL,
            raw_log TEXT
        )
    ''')
    
    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            source_log_id INTEGER,
            status TEXT DEFAULT 'open',
            FOREIGN KEY (source_log_id) REFERENCES logs (id)
        )
    ''')
    
    # Create alert rules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alert_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            condition TEXT NOT NULL,
            severity TEXT NOT NULL,
            enabled INTEGER DEFAULT 1
        )
    ''')
    
    # Insert default alert rules
    cursor.execute('''
        SELECT COUNT(*) FROM alert_rules
    ''')
    if cursor.fetchone()[0] == 0:
        default_rules = [
            ('Failed Authentication', 'Multiple failed login attempts detected', 
             'auth_failure', 'high'),
            ('Suspicious Network Activity', 'Unusual outbound connections detected',
             'network_anomaly', 'medium'),
            ('Privilege Escalation', 'User privilege elevation detected',
             'privilege_escalation', 'critical')
        ]
        cursor.executemany('''
            INSERT INTO alert_rules (name, description, condition, severity)
            VALUES (?, ?, ?, ?)
        ''', default_rules)
    
    db.commit()
    db.close()

# Initialize database on startup
init_db()

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SOC-Lite Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .header {
            background-color: #2d2d2d;
            padding: 20px;
            border-bottom: 3px solid #00ff00;
        }
        .header h1 {
            margin: 0;
            color: #00ff00;
        }
        .container {
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .nav {
            background-color: #2d2d2d;
            padding: 10px 20px;
            margin-bottom: 20px;
        }
        .nav a {
            color: #00ff00;
            text-decoration: none;
            margin-right: 20px;
            padding: 8px 16px;
            border: 1px solid #00ff00;
            border-radius: 4px;
            display: inline-block;
        }
        .nav a:hover {
            background-color: #00ff00;
            color: #1a1a1a;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #00ff00;
        }
        .stat-card h3 {
            margin: 0 0 10px 0;
            color: #00ff00;
            font-size: 14px;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
        }
        .section {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .section h2 {
            margin-top: 0;
            color: #00ff00;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th {
            background-color: #3d3d3d;
            color: #00ff00;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #00ff00;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #3d3d3d;
        }
        tr:hover {
            background-color: #3d3d3d;
        }
        .severity-critical { color: #ff3333; font-weight: bold; }
        .severity-high { color: #ff9933; font-weight: bold; }
        .severity-medium { color: #ffff33; }
        .severity-low { color: #33ff33; }
        .severity-info { color: #3399ff; }
        .status-open { color: #ff9933; }
        .status-investigating { color: #ffff33; }
        .status-resolved { color: #33ff33; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ SOC-Lite Dashboard</h1>
        <p>Security Operations Center - Real-time Monitoring</p>
    </div>
    
    <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/admin">Admin Panel</a>
        <a href="/simulate_alert/auth_failure">Simulate Alert</a>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3>TOTAL LOGS</h3>
                <div class="value">{{ stats.total_logs }}</div>
            </div>
            <div class="stat-card">
                <h3>OPEN ALERTS</h3>
                <div class="value">{{ stats.open_alerts }}</div>
            </div>
            <div class="stat-card">
                <h3>CRITICAL ALERTS</h3>
                <div class="value">{{ stats.critical_alerts }}</div>
            </div>
            <div class="stat-card">
                <h3>LOGS TODAY</h3>
                <div class="value">{{ stats.logs_today }}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Recent Alerts</h2>
            {% if alerts %}
            <table>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Description</th>
                    <th>Status</th>
                </tr>
                {% for alert in alerts %}
                <tr>
                    <td>{{ alert.id }}</td>
                    <td>{{ alert.timestamp }}</td>
                    <td>{{ alert.alert_type }}</td>
                    <td class="severity-{{ alert.severity }}">{{ alert.severity|upper }}</td>
                    <td>{{ alert.description }}</td>
                    <td class="status-{{ alert.status }}">{{ alert.status|upper }}</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>No alerts found. System is running normally.</p>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>Recent Logs</h2>
            {% if logs %}
            <table>
                <tr>
                    <th>ID</th>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Severity</th>
                    <th>Event Type</th>
                    <th>Message</th>
                </tr>
                {% for log in logs %}
                <tr>
                    <td>{{ log.id }}</td>
                    <td>{{ log.timestamp }}</td>
                    <td>{{ log.source }}</td>
                    <td class="severity-{{ log.severity }}">{{ log.severity|upper }}</td>
                    <td>{{ log.event_type or 'N/A' }}</td>
                    <td>{{ log.message[:100] }}{% if log.message|length > 100 %}...{% endif %}</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>No logs ingested yet. Use the /ingest endpoint to send logs.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SOC-Lite Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .header {
            background-color: #2d2d2d;
            padding: 20px;
            border-bottom: 3px solid #00ff00;
        }
        .header h1 {
            margin: 0;
            color: #00ff00;
        }
        .container {
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .nav {
            background-color: #2d2d2d;
            padding: 10px 20px;
            margin-bottom: 20px;
        }
        .nav a {
            color: #00ff00;
            text-decoration: none;
            margin-right: 20px;
            padding: 8px 16px;
            border: 1px solid #00ff00;
            border-radius: 4px;
            display: inline-block;
        }
        .nav a:hover {
            background-color: #00ff00;
            color: #1a1a1a;
        }
        .section {
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .section h2 {
            margin-top: 0;
            color: #00ff00;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th {
            background-color: #3d3d3d;
            color: #00ff00;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #00ff00;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #3d3d3d;
        }
        tr:hover {
            background-color: #3d3d3d;
        }
        .enabled { color: #33ff33; }
        .disabled { color: #ff3333; }
        .code-block {
            background-color: #1a1a1a;
            padding: 15px;
            border-radius: 4px;
            border: 1px solid #3d3d3d;
            overflow-x: auto;
        }
        .code-block pre {
            margin: 0;
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔧 SOC-Lite Admin Panel</h1>
        <p>Alert Rules & System Configuration</p>
    </div>
    
    <div class="nav">
        <a href="/">Dashboard</a>
        <a href="/admin">Admin Panel</a>
        <a href="/simulate_alert/auth_failure">Simulate Alert</a>
    </div>
    
    <div class="container">
        <div class="section">
            <h2>Alert Rules</h2>
            {% if rules %}
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Condition</th>
                    <th>Severity</th>
                    <th>Status</th>
                </tr>
                {% for rule in rules %}
                <tr>
                    <td>{{ rule.id }}</td>
                    <td>{{ rule.name }}</td>
                    <td>{{ rule.description }}</td>
                    <td><code>{{ rule.condition }}</code></td>
                    <td>{{ rule.severity|upper }}</td>
                    <td class="{% if rule.enabled %}enabled{% else %}disabled{% endif %}">
                        {{ 'ENABLED' if rule.enabled else 'DISABLED' }}
                    </td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>No alert rules configured.</p>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>API Documentation</h2>
            
            <h3>Ingest Logs (POST /ingest)</h3>
            <p>Send log data to the SOC system for processing and analysis.</p>
            <div class="code-block">
                <pre>curl -X POST http://localhost:5000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source": "firewall-01",
    "severity": "high",
    "event_type": "auth_failure",
    "message": "Failed login attempt from 192.168.1.100"
  }'</pre>
            </div>
            
            <h3>Simulate Alert (GET /simulate_alert/&lt;type&gt;)</h3>
            <p>Trigger a test alert for demonstration purposes.</p>
            <div class="code-block">
                <pre>curl http://localhost:5000/simulate_alert/auth_failure</pre>
            </div>
            <p>Available alert types: <code>auth_failure</code>, <code>network_anomaly</code>, <code>privilege_escalation</code></p>
        </div>
        
        <div class="section">
            <h2>System Statistics</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Logs Ingested</td>
                    <td>{{ stats.total_logs }}</td>
                </tr>
                <tr>
                    <td>Total Alerts Generated</td>
                    <td>{{ stats.total_alerts }}</td>
                </tr>
                <tr>
                    <td>Open Alerts</td>
                    <td>{{ stats.open_alerts }}</td>
                </tr>
                <tr>
                    <td>Active Alert Rules</td>
                    <td>{{ stats.active_rules }}</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    """Main dashboard showing recent logs and alerts."""
    db = get_db()
    cursor = db.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as count FROM logs')
    total_logs = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE status = 'open'")
    open_alerts = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE severity = 'critical' AND status = 'open'")
    critical_alerts = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM logs WHERE date(timestamp) = date('now')")
    logs_today = cursor.fetchone()['count']
    
    stats = {
        'total_logs': total_logs,
        'open_alerts': open_alerts,
        'critical_alerts': critical_alerts,
        'logs_today': logs_today
    }
    
    # Get recent alerts
    cursor.execute('''
        SELECT * FROM alerts 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''')
    alerts = cursor.fetchall()
    
    # Get recent logs
    cursor.execute('''
        SELECT * FROM logs 
        ORDER BY timestamp DESC 
        LIMIT 20
    ''')
    logs = cursor.fetchall()
    
    db.close()
    
    return render_template_string(HOME_TEMPLATE, stats=stats, alerts=alerts, logs=logs)

@app.route('/ingest', methods=['POST'])
def ingest():
    """Ingest log data via REST API."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        source = data.get('source', 'unknown')
        severity = data.get('severity', 'info')
        event_type = data.get('event_type', '')
        message = data.get('message', '')
        raw_log = data.get('raw_log', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # Insert log
        cursor.execute('''
            INSERT INTO logs (source, severity, event_type, message, raw_log)
            VALUES (?, ?, ?, ?, ?)
        ''', (source, severity, event_type, message, raw_log))
        
        log_id = cursor.lastrowid
        
        # Check if we should generate an alert based on event_type
        if event_type:
            cursor.execute('''
                SELECT * FROM alert_rules 
                WHERE condition = ? AND enabled = 1
            ''', (event_type,))
            rule = cursor.fetchone()
            
            if rule:
                # Generate alert
                cursor.execute('''
                    INSERT INTO alerts (alert_type, severity, description, source_log_id)
                    VALUES (?, ?, ?, ?)
                ''', (rule['name'], rule['severity'], 
                      f"{rule['description']} - {message[:100]}", log_id))
        
        db.commit()
        db.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Log ingested successfully',
            'log_id': log_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    """Admin panel for managing alert rules and viewing system stats."""
    db = get_db()
    cursor = db.cursor()
    
    # Get all alert rules
    cursor.execute('SELECT * FROM alert_rules ORDER BY id')
    rules = cursor.fetchall()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as count FROM logs')
    total_logs = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM alerts')
    total_alerts = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE status = 'open'")
    open_alerts = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM alert_rules WHERE enabled = 1')
    active_rules = cursor.fetchone()['count']
    
    stats = {
        'total_logs': total_logs,
        'total_alerts': total_alerts,
        'open_alerts': open_alerts,
        'active_rules': active_rules
    }
    
    db.close()
    
    return render_template_string(ADMIN_TEMPLATE, rules=rules, stats=stats)

@app.route('/simulate_alert/<alert_type>')
def simulate_alert(alert_type):
    """Simulate an alert for demonstration purposes."""
    db = get_db()
    cursor = db.cursor()
    
    # Create a simulated log entry
    simulations = {
        'auth_failure': {
            'source': 'server-01',
            'severity': 'high',
            'event_type': 'auth_failure',
            'message': 'SIMULATION: Multiple failed login attempts detected from IP 192.168.1.100 (user: admin)'
        },
        'network_anomaly': {
            'source': 'firewall-01',
            'severity': 'medium',
            'event_type': 'network_anomaly',
            'message': 'SIMULATION: Unusual outbound connection to suspicious IP 45.33.32.156:443'
        },
        'privilege_escalation': {
            'source': 'server-02',
            'severity': 'critical',
            'event_type': 'privilege_escalation',
            'message': 'SIMULATION: User account "jdoe" elevated to administrative privileges'
        }
    }
    
    if alert_type not in simulations:
        return jsonify({'error': 'Invalid alert type'}), 400
    
    sim = simulations[alert_type]
    
    # Insert simulated log
    cursor.execute('''
        INSERT INTO logs (source, severity, event_type, message, raw_log)
        VALUES (?, ?, ?, ?, ?)
    ''', (sim['source'], sim['severity'], sim['event_type'], sim['message'], 
          f"SIMULATED LOG: {sim['message']}"))
    
    log_id = cursor.lastrowid
    
    # Get matching alert rule
    cursor.execute('''
        SELECT * FROM alert_rules 
        WHERE condition = ? AND enabled = 1
    ''', (sim['event_type'],))
    rule = cursor.fetchone()
    
    alert_id = None
    if rule:
        # Generate alert
        cursor.execute('''
            INSERT INTO alerts (alert_type, severity, description, source_log_id)
            VALUES (?, ?, ?, ?)
        ''', (rule['name'], rule['severity'], 
              f"SIMULATED: {rule['description']} - {sim['message']}", log_id))
        alert_id = cursor.lastrowid
    
    db.commit()
    db.close()
    
    return jsonify({
        'status': 'success',
        'message': f'Simulated {alert_type} alert created',
        'log_id': log_id,
        'alert_id': alert_id
    })

if __name__ == '__main__':
    print("=" * 60)
    print("SOC-Lite Prototype Server Starting...")
    print("=" * 60)
    print("\nDashboard: http://localhost:5000/")
    print("Admin Panel: http://localhost:5000/admin")
    print("\nAPI Endpoints:")
    print("  POST /ingest - Ingest log data")
    print("  GET  /simulate_alert/<type> - Simulate alerts")
    print("\nExample:")
    print('  curl -X POST http://localhost:5000/ingest \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"source":"test","severity":"high","event_type":"auth_failure","message":"Test log"}\'')
    print("\n" + "=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
