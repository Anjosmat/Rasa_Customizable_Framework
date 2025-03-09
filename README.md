# Rasa Customizable Framework - Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Installation Guide](#2-installation-guide)
3. [Configuration Setup](#3-configuration-setup)
4. [Workflow & Logic](#4-workflow--logic)
5. [Usage Instructions](#5-usage-instructions)
6. [How to Extend or Customize](#6-how-to-extend-or-customize)
7. [Deployment Guide](#7-deployment-guide)
8. [Troubleshooting](#8-troubleshooting)
9. [Known Limitations](#9-known-limitations)
10. [Contributing Guidelines](#10-contributing-guidelines)
11. [Version Information](#11-version-information)
12. [Security Considerations](#12-security-considerations)
13. [Support and Community](#13-support-and-community)

## 1. Project Overview
This project is a generic Rasa-based chatbot framework that allows businesses to configure and customize their own chatbots dynamically. Instead of hardcoded intents, this framework loads intents from a database, making it adaptable for different industries and use cases.

### Key Features
- Dynamic intent management via database
- Multi-business support
- Customizable response handling
- Scalable architecture
- Docker support
- Cloud-ready deployment options

## 2. Installation Guide
### Prerequisites
- Python 3.10 or higher
- Git
- Rasa CLI (`pip install rasa`)
- Virtual Environment (recommended)

### Setup Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Anjosmat/Rasa_Customizable_Framework.git
   cd Rasa_Customizable_Framework
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/MacOS
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   python database/setup_db.py
   ```

5. **Train the Model**
   ```bash
   rasa train
   ```

6. **Start the Services**
   ```bash
   # Terminal 1
   rasa run
   # Terminal 2
   rasa run actions
   ```

## 3. Configuration Setup
- Edit `config.yml` for NLU pipeline settings
- Modify `domain.yml` for core functionality
- Configure database settings in `database/db_config.py`

## 4. Workflow & Logic
1. **Intent Processing**
   - User input → NLU processing
   - Intent extraction & classification
   - Database query for response

2. **Response Generation**
   - Dynamic response fetching
   - Fallback handling
   - Context management

## 5. Usage Instructions
### Basic Operations
```bash
# Start Rasa server
rasa run

# Start Action server
rasa run actions

# Interactive shell
rasa shell
```

### Managing Intents
1. Access SQLite database
2. Add/modify intents in business_intents table
3. Restart services

## 6. How to Extend or Customize
- Add custom actions in `actions/actions.py`
- Implement new database queries
- Create business-specific intent filters

## 7. Deployment Guide
### Docker Deployment
```dockerfile
FROM rasa/rasa:latest
COPY . /app
WORKDIR /app
RUN rasa train
CMD ["rasa", "run", "--enable-api"]
```

### Cloud Deployment
- AWS EC2 recommended setup
- Database migration guidelines
- Load balancing configurations

## 8. Troubleshooting
| Issue | Solution |
|-------|----------|
| Port conflicts | Check running processes, use alternative ports |
| Training failures | Verify dependencies and Python version |
| Database connection issues | Check credentials and connectivity |

## 9. Known Limitations
- Concurrent user threshold: 1000 users/minute
- SQLite limitations for high loads
- English language optimization
- Training time scales with intent volume

## 10. Contributing Guidelines
1. Fork repository
2. Create feature branch
3. Follow coding standards
4. Submit pull request

## 11. Version Information
- Version: 1.0.0
- Last Updated: 2024
- Rasa Compatibility: 3.x
- Python: 3.10+

## 12. Security Considerations
- Regular security updates
- API authentication required
- Database access restrictions
- Rate limiting implementation

## 13. Support and Community
- GitHub Issues for bug reports
- Feature requests via pull requests
- Community discussions in Discussions tab
- Documentation contributions welcome

---
© 2024 Rasa Customizable Framework. All rights reserved.