# Rasa Customizable Agentic Chatbot Framework

A modular, database-driven agentic chatbot framework built on Rasa, with a front-end UI for business owners and admins to interact with the chatbot and manage configurations.

## Key Features

- **Agentic AI**: The chatbot autonomously responds to user input based on stored logic.
- **Database-Driven**: Custom chatbot behaviors are stored in a database, eliminating the need for code modifications.
- **Scalable & Modular**: Businesses can configure their chatbot through a UI without modifying the core structure.
- **Admin Portal**: Manage businesses, users, and chatbot configurations via a web-based interface.
- **Frontend UI for Interaction**: A chat interface where businesses, admins, and customers can interact with the chatbot.
- **APIs & Webhooks**: Enables easy integration with external applications.

## Project Structure

```
Rasa_Customizable_Framework/
│
├── actions/                  # Rasa custom actions
│   ├── __init__.py
│   └── actions.py            # Custom actions to fetch responses from DB
│
├── admin/                    # Admin portal
│   ├── __init__.py
│   ├── models.py             # Admin user models
│   ├── routes.py             # Admin routes
│   └── templates/            # Admin templates
│
├── database/                 # Database management
│   ├── __init__.py
│   ├── db_config.py          # Database configuration
│   ├── models.py             # Database models (merged with db_config.py)
│   └── load_data.py          # Sample data loader
│
├── static/                   # Static files (CSS, JS)
│   ├── css/
│   └── js/
│
├── templates/                # Frontend templates
│   ├── admin/                # Admin templates
│   ├── index.html            # Chat interface
│   └── login.html            # Login page
│
├── .env                      # Environment variables
├── app.py                    # Main Flask application
├── config.yml                # Rasa configuration
├── credentials.yml           # Rasa credentials
├── domain.yml                # Rasa domain
├── endpoints.yml             # Rasa endpoints
├── init_project.py           # Project initialization script
└── requirements.txt          # Project dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)
- SQLite (included in Python)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Anjosmat/Rasa_Customizable_Framework.git
   cd Rasa_Customizable_Framework
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Run the initialization script:
   ```
   python init_project.py
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Train the Rasa model:
   ```
   rasa train
   ```

### Running the Application

You'll need three terminal windows for running the full application:

1. **Terminal 1**: Run the Flask web application
   ```
   flask run
   ```
   This will start the web server at http://localhost:5000

2. **Terminal 2**: Run the Rasa Action Server
   ```
   rasa run actions
   ```
   This will start the action server at http://localhost:5055

3. **Terminal 3**: Run the Rasa API Server
   ```
   rasa run --enable-api
   ```
   This will start the Rasa server at http://localhost:5005

### Admin Access

Once the application is running, you can access the admin portal at http://localhost:5000/login with the following credentials:

- **Email**: admin@example.com
- **Password**: admin123

## Usage

### Managing Businesses

1. Log in to the admin portal
2. Navigate to the "Businesses" section
3. Add, edit, or remove businesses

### Managing Intents

1. Log in to the admin portal
2. Navigate to the "Intents" section
3. Add, edit, or remove intents and their responses

### Using the Chatbot

1. Access the chat interface at http://localhost:5000
2. Select a business type from the options
3. Start chatting with the bot

## Development

### Adding New Business Types

1. Add a new business in the admin portal
2. Define intents and responses specific to that business type
3. Configure the chatbot settings for the new business

### Adding New Intents

1. Log in to the admin portal
2. Navigate to the "Intents" section
3. Click "Add New Intent"
4. Fill in the business type, intent name, response, and training examples
5. Save the intent

### Customizing Bot Responses

1. Log in to the admin portal
2. Navigate to the "Intents" section
3. Edit the intent you want to customize
4. Update the response text
5. Save your changes

## Extending the Framework

### Adding New Features

To add new features to the chatbot:

1. Create new custom actions in `actions/actions.py`
2. Add new intent patterns in the admin portal
3. Update the `domain.yml` to include new actions if needed
4. Retrain the model: `rasa train`

### Database Schema

The framework uses the following database tables:

- `business_intents`: Stores intents and responses for each business type
- `bot_config`: Stores configuration settings for each business type
- `businesses`: Stores business information
- `admin_users`: Stores admin user accounts
- `chatbot_logs`: Stores conversation logs

## Roadmap

Future enhancements planned for this framework:

- Advanced NLU with entity extraction
- Conversational memory (context-aware responses)
- Webhook integrations for third-party services
- Multi-tenant architecture for SaaS deployment
- Analytics dashboard with conversation insights
- Multilingual support

## Troubleshooting

### Common Issues

**Rasa server not responding:**
- Make sure the Rasa server is running (`rasa run --enable-api`)
- Check the Rasa server logs for any errors

**Actions not working:**
- Ensure the action server is running (`rasa run actions`)
- Check that your custom actions are properly defined in `actions/actions.py`

**Database errors:**
- Verify that the database file exists at `database/business_data.db`
- Run the initialization script again if needed: `python init_project.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Rasa](https://rasa.com/) for the open-source conversational AI framework
- [Flask](https://flask.palletsprojects.com/) for the web application framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM