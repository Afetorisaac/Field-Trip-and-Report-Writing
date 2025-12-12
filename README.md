# Field-Trip-and-Report-Writing

## Phishing Simulation and Security Awareness Training Platform

This repository contains the comprehensive documentation, diagrams, and a functional prototype for a Phishing Simulation and Security Awareness Training Platform.

## Repository Contents

### 📄 Reports
- **reports/Report1_Final.md** - Complete technical report covering:
  - Executive summary and introduction
  - System architecture and technology stack
  - Functional and non-functional requirements
  - Implementation plan and risk assessment
  - Testing strategy
  - References

### 📊 Diagrams
- **diagrams/report1_system_architecture.mmd** - System architecture diagram showing the three-tier architecture
- **diagrams/report1_use_case.mmd** - Use case diagram illustrating user interactions
- **diagrams/report1_sequence.mmd** - Sequence diagram for campaign creation and execution flow

All diagrams are in Mermaid format and can be visualized using any Mermaid-compatible viewer.

### 🚀 Prototype
A minimal Flask-based prototype demonstrating core platform features:

#### Files
- **prototype/app.py** - Flask application with database initialization and routes
- **prototype/requirements.txt** - Python dependencies
- **prototype/templates/** - HTML templates for all pages:
  - `index.html` - Landing page
  - `admin.html` - Admin dashboard
  - `simulate.html` - Campaign creation interface
  - `landing.html` - Post-click awareness page

## Running the Prototype

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Afetorisaac/Field-Trip-and-Report-Writing.git
cd Field-Trip-and-Report-Writing
```

2. Navigate to the prototype directory:
```bash
cd prototype
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

### Using the Prototype

#### Home Page (`/`)
- View feature overview
- Navigate to Admin Dashboard or Campaign Creation

#### Admin Dashboard (`/admin`)
- View statistics (total users, campaigns, clicks)
- See recent campaigns
- Quick access to create new campaigns

#### Create Campaign (`/simulate`)
- Configure a new phishing simulation campaign
- Select from pre-defined email templates
- Preview template content
- Launch campaigns

#### Landing Page (`/landing/<campaign_id>`)
- Educational page shown after clicking simulated phishing link
- Provides tips on identifying phishing emails
- Logs user interaction for reporting

#### API Endpoints
- `GET /api/stats` - Returns campaign performance statistics
- `GET /courses` - Lists available training courses

### Database
The prototype uses SQLite for simplicity. The database (`phishing_demo.db`) is automatically created on first run with sample data including:
- 3 sample users (1 admin, 2 regular users)
- 3 sample training courses

## Architecture Overview

The platform is designed with a modern three-tier architecture:

- **Presentation Layer**: React-based front-end (production version)
- **Application Layer**: Django REST API (production version) / Flask (prototype)
- **Data Layer**: PostgreSQL (production version) / SQLite (prototype)

The prototype demonstrates the core concepts using lightweight technologies suitable for demonstration purposes.

## Features Demonstrated

✅ User and role management  
✅ Campaign creation and configuration  
✅ Email template selection  
✅ Click tracking and interaction logging  
✅ Admin dashboard with statistics  
✅ Educational landing pages  
✅ Basic reporting API  

## Development Notes

This prototype is for **demonstration purposes only** and includes:
- Simplified authentication (no actual auth implemented)
- SQLite database (production would use PostgreSQL)
- No actual email sending (production uses SMTP integration)
- Basic styling (production uses React with Material-UI)

The full production system will include additional features such as:
- Comprehensive user authentication and authorization
- Email delivery with tracking
- Advanced analytics and reporting
- Interactive training modules with quizzes
- Scheduled campaign execution
- Department-level management
- Notification system

## Contributing

This project is part of an academic exercise. For questions or contributions, please contact the repository maintainer.

## License

This project is created for educational purposes as part of a field trip and report writing assignment.

## Notes

⚠️ **Important**: This PR should remain unmerged pending review and approval of the documentation and prototype design.