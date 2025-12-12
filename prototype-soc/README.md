# SOC-Lite Prototype

A minimal Security Operations Center (SOC) demonstration system for log ingestion, alert management, and security monitoring.

## Overview

This prototype demonstrates core SIEM (Security Information and Event Management) functionality including:

- **Log Ingestion**: REST API endpoint for receiving logs from various sources
- **Alert Generation**: Automatic alert creation based on predefined rules
- **Dashboard**: Real-time visualization of security events and alerts
- **Admin Panel**: Alert rule management and system statistics

## Features

### 1. Log Ingestion API
- Accepts logs via POST requests in JSON format
- Stores logs in SQLite database
- Automatically triggers alerts based on event types

### 2. Alert System
- Predefined alert rules for common security events
- Alert severities: Critical, High, Medium, Low, Info
- Alert statuses: Open, Investigating, Resolved

### 3. Dashboard
- Real-time statistics (total logs, open alerts, critical alerts)
- Recent alerts display
- Recent logs display with severity highlighting

### 4. Admin Panel
- View all configured alert rules
- System statistics and metrics
- API documentation

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Navigate to the prototype-soc directory:
```bash
cd prototype-soc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the dashboard:
- Dashboard: http://localhost:5000/
- Admin Panel: http://localhost:5000/admin

## Usage

### Viewing the Dashboard

Navigate to `http://localhost:5000/` to see:
- Current system statistics
- Recent security alerts
- Recent log entries

### Ingesting Logs

Send logs to the system using the REST API:

```bash
curl -X POST http://localhost:5000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source": "firewall-01",
    "severity": "high",
    "event_type": "auth_failure",
    "message": "Failed login attempt from 192.168.1.100"
  }'
```

#### Log Fields

| Field | Required | Description | Example Values |
|-------|----------|-------------|----------------|
| `source` | No | System or device that generated the log | "firewall-01", "server-web-01" |
| `severity` | No | Log severity level | "critical", "high", "medium", "low", "info" |
| `event_type` | No | Type of security event | "auth_failure", "network_anomaly", "privilege_escalation" |
| `message` | Yes | Log message content | "Failed login attempt detected" |
| `raw_log` | No | Original raw log data | Full syslog line |

### Simulating Alerts

For demonstration purposes, you can simulate alerts:

```bash
# Simulate authentication failure
curl http://localhost:5000/simulate_alert/auth_failure

# Simulate network anomaly
curl http://localhost:5000/simulate_alert/network_anomaly

# Simulate privilege escalation
curl http://localhost:5000/simulate_alert/privilege_escalation
```

Or use the dashboard navigation button to simulate alerts through the web interface.

### Managing Alert Rules

Access the Admin Panel at `http://localhost:5000/admin` to:
- View all configured alert rules
- See which rules are enabled/disabled
- Review system statistics

## Default Alert Rules

The system comes preconfigured with three alert rules:

1. **Failed Authentication**
   - Condition: `event_type == "auth_failure"`
   - Severity: High
   - Description: Multiple failed login attempts detected

2. **Suspicious Network Activity**
   - Condition: `event_type == "network_anomaly"`
   - Severity: Medium
   - Description: Unusual outbound connections detected

3. **Privilege Escalation**
   - Condition: `event_type == "privilege_escalation"`
   - Severity: Critical
   - Description: User privilege elevation detected

## Database Schema

The prototype uses SQLite with three main tables:

### logs
- `id`: Primary key
- `timestamp`: Log creation time
- `source`: Origin system
- `severity`: Log severity level
- `event_type`: Categorized event type
- `message`: Log message
- `raw_log`: Original log data

### alerts
- `id`: Primary key
- `timestamp`: Alert creation time
- `alert_type`: Type of alert
- `severity`: Alert severity
- `description`: Alert description
- `source_log_id`: Foreign key to logs table
- `status`: Alert status (open/investigating/resolved)

### alert_rules
- `id`: Primary key
- `name`: Rule name
- `description`: Rule description
- `condition`: Matching condition
- `severity`: Alert severity to assign
- `enabled`: Whether rule is active

## Architecture

```
┌─────────────────┐
│  Data Sources   │
│  (Logs)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  REST API       │
│  /ingest        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite DB      │
│  (Storage)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask App      │
│  (Processing)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Web Dashboard  │
│  (Visualization)│
└─────────────────┘
```

## API Reference

### POST /ingest
Ingest log data into the system.

**Request Body:**
```json
{
  "source": "string",
  "severity": "string",
  "event_type": "string",
  "message": "string",
  "raw_log": "string"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Log ingested successfully",
  "log_id": 123
}
```

### GET /
Main dashboard displaying statistics, recent alerts, and logs.

### GET /admin
Admin panel with alert rules and system configuration.

### GET /simulate_alert/<type>
Simulate a specific type of alert for testing.

**Parameters:**
- `type`: One of "auth_failure", "network_anomaly", "privilege_escalation"

**Response:**
```json
{
  "status": "success",
  "message": "Simulated auth_failure alert created",
  "log_id": 123,
  "alert_id": 45
}
```

## Limitations

This is a demonstration prototype and has several limitations:

- **Not Production-Ready**: Lacks authentication, authorization, and many security features
- **SQLite Database**: Not suitable for high-volume log ingestion
- **No Distributed Processing**: Single-threaded Flask development server
- **Basic Alert Logic**: Simple rule matching without complex correlation
- **No Data Retention Policies**: Logs accumulate indefinitely
- **Limited Visualization**: Basic HTML tables instead of advanced charts

## Future Enhancements

Potential improvements for a production system:

1. **Authentication & Authorization**: Implement user login and role-based access control
2. **Database Upgrade**: Use PostgreSQL or Elasticsearch for scalability
3. **Advanced Correlation**: Multi-event pattern matching and anomaly detection
4. **Enhanced Visualization**: Add charts, graphs, and interactive dashboards
5. **Real Integrations**: Connect to actual log sources (Filebeat, syslog, etc.)
6. **Alert Actions**: Email notifications, webhook integrations, automated responses
7. **Data Retention**: Implement log archival and deletion policies
8. **API Security**: Add API key authentication and rate limiting
9. **High Availability**: Clustering and load balancing support
10. **Machine Learning**: Behavioral analysis and threat detection

## Related Documentation

For more information about the SOC concept and architecture, see:
- `../reports/Report2_Final.md` - Complete report on SOC implementation
- `../diagrams/report2_system_architecture.mmd` - System architecture diagram
- `../diagrams/report2_use_case.mmd` - Use case diagram
- `../diagrams/report2_sequence.mmd` - Sequence diagram

## License

This is a demonstration prototype for educational purposes.

## Contributing

This prototype is part of a field trip report and is not actively maintained for external contributions.

## Support

For questions or issues, refer to the main repository documentation.
