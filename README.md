# Field Trip and Report Writing - Human-Layer Security Challenge

This repository contains a comprehensive research report and interactive prototype for addressing human-layer security vulnerabilities in cybersecurity systems.

## 📚 Repository Contents

### 1. Reports
- **`reports/Report1_Final.md`** - Complete research report on Human-Layer Security Challenge
  - Executive summary and introduction
  - Literature review of social engineering attacks
  - Methodology and research approach
  - System architecture and design
  - Implementation results and analysis
  - Comprehensive references

### 2. Diagrams
Mermaid diagram sources for visualizing the security training system:
- **`diagrams/report1_system_architecture.mmd`** - System architecture diagram
- **`diagrams/report1_use_case.mmd`** - Use case diagram
- **`diagrams/report1_sequence.mmd`** - Sequence diagram for user interactions

### 3. Prototype Application
A Flask-based web application for security awareness training:
- **`prototype/app.py`** - Main Flask application
- **`prototype/requirements.txt`** - Python dependencies
- **`prototype/templates/`** - HTML templates
  - `landing.html` - Login and registration page
  - `index.html` - User dashboard
  - `simulate.html` - Interactive simulation interface
  - `admin.html` - Administrative analytics dashboard

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- virtualenv (recommended)

### Installation and Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Afetorisaac/Field-Trip-and-Report-Writing.git
   cd Field-Trip-and-Report-Writing
   ```

2. **Navigate to the prototype directory**
   ```bash
   cd prototype
   ```

3. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**
   
   On Linux/macOS:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Default Credentials

The application comes with a default admin account:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Security Note:** Change these credentials in a production environment!

## 📖 Using the Prototype

### For Users (Learners)
1. **Register** a new account on the landing page
2. **Log in** with your credentials
3. **View your dashboard** to see available simulations and your progress
4. **Start a simulation** by clicking on any scenario
5. **Make your choice** based on the presented social engineering scenario
6. **Receive immediate feedback** on your decision
7. **Track your progress** over time

### For Administrators
1. **Log in** with admin credentials
2. **Access the Admin Panel** from the navigation bar
3. **View overall statistics** across all users
4. **Monitor individual user performance**
5. **Review recent activity** and trends

## 🎯 Features

### Core Functionality
- ✅ User registration and authentication
- ✅ Interactive social engineering simulations
- ✅ Immediate feedback and educational content
- ✅ Progress tracking and performance metrics
- ✅ Admin dashboard with analytics
- ✅ Automatic database initialization
- ✅ Responsive design for mobile devices

### Simulation Scenarios
The prototype includes four realistic scenarios:
1. **Phishing Email Detection** (Easy) - Identify fraudulent emails
2. **USB Drive in Parking Lot** (Medium) - Handle found media devices
3. **Social Engineering Phone Call** (Medium) - Respond to suspicious calls
4. **Tailgating at Building Entry** (Hard) - Manage physical security threats

## 🗂️ Database Schema

The application uses SQLite with three main tables:

- **users** - User accounts and authentication
- **simulations** - Security training scenarios
- **results** - User performance tracking

The database is automatically created on first run with sample data.

## 🔧 Technical Details

### Technology Stack
- **Backend:** Python Flask 3.0.0
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, vanilla JavaScript
- **Styling:** Custom CSS with gradient designs

### Project Structure
```
Field-Trip-and-Report-Writing/
├── README.md
├── reports/
│   └── Report1_Final.md
├── diagrams/
│   ├── report1_system_architecture.mmd
│   ├── report1_use_case.mmd
│   └── report1_sequence.mmd
└── prototype/
    ├── app.py
    ├── requirements.txt
    ├── security_training.db (created at runtime)
    └── templates/
        ├── landing.html
        ├── index.html
        ├── simulate.html
        └── admin.html
```

## 📊 Viewing Diagrams

The Mermaid diagrams can be viewed using:
- [Mermaid Live Editor](https://mermaid.live/)
- GitHub's built-in Mermaid rendering
- VS Code with Mermaid extension
- Any Markdown viewer that supports Mermaid syntax

## 🔐 Security Considerations

This is a **demonstration prototype** for educational purposes:

- Passwords are stored in plain text (use hashing in production)
- Session management is basic (implement secure sessions in production)
- No rate limiting or CAPTCHA (add for production use)
- Default secret key should be changed
- Consider HTTPS for production deployment
- Add input validation and sanitization
- Implement CSRF protection

## 🧪 Testing

To verify the application is working:

1. Start the application as described above
2. Register a new user account
3. Log in and complete at least one simulation
4. Log in as admin to view the analytics dashboard
5. Verify all pages load correctly and data persists

## 🛠️ Development

### Adding New Simulations

Edit `app.py` and add new scenarios to the simulations list in the `init_db()` function:

```python
{
    'title': 'Your Scenario Title',
    'description': 'Brief description',
    'scenario': 'Detailed scenario text',
    'correct_answer': 'report',  # or 'refuse', 'verify', etc.
    'difficulty': 'medium'  # 'easy', 'medium', or 'hard'
}
```

### Customizing the Interface

- Edit CSS in the template files to change colors and styling
- Modify the gradient colors by changing the `linear-gradient` values
- Adjust layouts by modifying the grid and flexbox properties

## 📝 Report Summary

The full research report (Report1_Final.md) covers:
- Analysis of human-layer security threats
- Cognitive biases exploited in social engineering
- Current defense mechanisms and their limitations
- Proposed security awareness framework
- Future enhancements and recommendations

## 👥 Contributing

This is an academic project. For suggestions or issues, please open an issue on GitHub.

## 📄 License

This project is provided for educational purposes.

## 📧 Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Last Updated:** December 2025  
**Version:** 1.0