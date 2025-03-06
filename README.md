Rasa Customizable Framework - Documentation
1. Project Overview
This project is a generic Rasa-based chatbot framework that allows businesses to configure and customize their own chatbots dynamically. Instead of hardcoded intents, this framework loads intents from a database, making it adaptable for different industries and use cases.

2. Installation Guide
Prerequisites
Before installing, ensure you have the following:

Python 3.10 (Check with python --version)
Git (Check with git --version)
Rasa CLI (Install with pip install rasa)
Virtual Environment (Optional but recommended)
Setup Steps
1. Clone the Repository
sh
Copy
Edit
git clone https://github.com/Anjosmat/Rasa_Customizable_Framework.git
cd Rasa_Customizable_Framework
2. Create & Activate Virtual Environment
sh
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # Windows
3. Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4. Setup the Database
Run:

sh
Copy
Edit
python database/setup_db.py
This initializes the SQLite database and creates required tables.

5. Train the Model
sh
Copy
Edit
rasa train
6. Start Rasa and Actions Server
Run the following in separate terminals:
Start Rasa:

sh
Copy
Edit
rasa run
Start Action Server:

sh
Copy
Edit
rasa run actions
3. Configuration Setup
The chatbot's settings are in the config.yml file.

Modify pipeline settings for NLU models.
Adjust policies for dialog management.
Change database configurations in database/db_config.py.
4. Workflow & Logic
1. User Sends a Message
Rasa receives the message and extracts intent using NLU.
Example: "hello" → Intent: greet.
2. Intent Matching with Database
The chatbot queries the SQLite database for a matching response.
If a match exists, it responds; otherwise, it triggers the fallback response.
3. Response Generation
Responses are fetched dynamically from the database.
If no response exists, the bot returns:
"I'm not sure how to respond to that."
4. Conversation Continues
Users interact with the bot based on the pre-configured or dynamically loaded intents.
5. Usage Instructions
Start the Chatbot
Run the Rasa server
sh
Copy
Edit
rasa run
Start the action server
sh
Copy
Edit
rasa run actions
Chat with the bot
sh
Copy
Edit
rasa shell
Adding New Intents
To add new responses dynamically:

Open SQLite database.
Insert new intents into the business_intents table.
Restart the chatbot to apply changes.
6. How to Extend or Customize
1. Adding More Intents
Add new intent names and responses to the database.
No need to modify domain.yml since responses are loaded dynamically.
2. Adding Custom Actions
Implement logic in actions/actions.py.
Register new actions in domain.yml.
3. Supporting Different Business Types
Each business can have its own set of intents.
Customize by filtering database queries based on business type.
7. Deployment Guide
1. Docker Deployment
Create a Dockerfile:
dockerfile
Copy
Edit
FROM rasa/rasa:latest
COPY . /app
WORKDIR /app
RUN rasa train
CMD ["rasa", "run", "--enable-api"]
Build and run:
sh
Copy
Edit
docker build -t rasa-bot .
docker run -p 5005:5005 rasa-bot
2. Deploying on a Cloud Server
Use AWS EC2, Google Cloud Run, or Azure.
Set up a PostgreSQL database for production use.
3. Running as a Background Service
Use nohup or pm2 to keep the bot running:

sh
Copy
Edit
nohup rasa run &
nohup rasa run actions &
8. Troubleshooting
Issue	Solution
OSError: [Errno 10048]	Port 5055 is already in use. Run `netstat -ano
rasa train fails	Ensure all dependencies are installed via pip install -r requirements.txt
Failed to execute custom action	Ensure the action server is running with rasa run actions
This documentation should now be ready for use. Let me know when you're ready to move to the next step! 🚀

You said:
done
ChatGPT said:
Now, let's push the latest changes to GitHub.

1. Check for Changes
Run the following to see which files have been modified:

sh
Copy
Edit
git status
2. Add All Changes
sh
Copy
Edit
git add .
3. Commit the Changes
Use a meaningful commit message:

sh
Copy
Edit
git commit -m "Updated project packaging and documentation"
4. Push to GitHub
sh
Copy
Edit
git push origin master
If you're using the main branch instead of master, use:

sh
Copy
Edit
git push origin main
Once you have successfully pushed the changes, type done to move to the next step. 🚀

You said:
done
ChatGPT said:
Now, let's generate the detailed documentation for your bot.

Steps for Documentation
The documentation will include:

Project Overview

What the bot does.
How it is structured.
Installation & Setup Guide

Prerequisites.
How to install dependencies and set up the environment.
How to Run the Bot

Commands for training, running actions, and testing.
Database Integration

How the bot retrieves and updates responses dynamically.
Workflow & Logic

Flow of how the bot processes user input and fetches responses.
Customizing the Bot

How to add new responses and modify settings.
Deployment Guide

Options for deploying on a server or as a service.
I'll generate the documentation now. Once done, I'll provide you with a markdown file (README.md) and paste the full documentation here. Stay tuned! 🚀

Here is the detailed documentation for your bot.

Rasa Customizable Bot Framework
1. Overview
This is a generic, database-driven chatbot built using Rasa. It is designed to be easily configurable so that you can quickly modify responses for different business use cases without changing the code.

The chatbot:

Uses SQLite for storing and retrieving intents dynamically.
Supports custom actions to fetch responses from the database.
Is designed to be extensible, allowing future enhancements like API integrations.
2. Installation & Setup Guide
2.1 Prerequisites
Ensure you have the following installed:

Python 3.10
Git (for version control)
SQLite (bundled with Python)
Rasa framework
2.2 Clone the Repository
sh
Copy
Edit
git clone https://github.com/Anjosmat/Rasa_Customizable_Framework.git
cd Rasa_Customizable_Framework
2.3 Set Up a Virtual Environment
sh
Copy
Edit
python -m venv .venv
Activate the virtual environment:

Windows (Command Prompt):
sh
Copy
Edit
.venv\Scripts\activate
Windows (PowerShell):
sh
Copy
Edit
.venv\Scripts\Activate.ps1
2.4 Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3. Running the Bot
3.1 Start the Rasa Action Server
sh
Copy
Edit
rasa run actions
3.2 Train the Model
sh
Copy
Edit
rasa train
3.3 Start the Bot
sh
Copy
Edit
rasa shell
4. Database Integration
4.1 How Responses Are Stored
The bot dynamically retrieves responses from the SQLite database. The table business_intents contains:

intent_name: The name of the intent (e.g., greet, goodbye).
response_text: The bot's response.
4.2 Checking Existing Responses
You can inspect stored intents with:

sh
Copy
Edit
sqlite3 database/business_data.db
SELECT * FROM business_intents;
4.3 Adding New Responses
New intents can be inserted using:

sql
Copy
Edit
INSERT INTO business_intents (intent_name, response_text) VALUES ('thank_you', 'You're welcome!');
5. Workflow & Logic
5.1 Bot Processing Flow
User Input → Rasa interprets the intent.
Custom Action (action_respond_from_db) retrieves the correct response from SQLite.
Bot Response → The bot replies dynamically.
5.2 Key Components
actions.py → Defines the logic for fetching responses from the database.
db_config.py → Manages database connections.
models.py → Defines database table schemas.
6. Customizing the Bot
6.1 Adding a New Intent
Insert new intents in the database (business_intents table).
Train the Rasa model:
sh
Copy
Edit
rasa train
Restart the bot.
6.2 Changing the Default Response
Modify responses directly in the database:

sql
Copy
Edit
UPDATE business_intents SET response_text='New response here' WHERE intent_name='greet';
7. Deployment Guide
The bot can be deployed on:

Docker

Build an image with:
sh
Copy
Edit
docker build -t rasa-bot .
Run the bot:
sh
Copy
Edit
docker run -p 5005:5005 rasa-bot
Cloud (AWS, Azure, GCP)

Deploy using Rasa X for cloud-based management.
Connect a webhook for real-time interactions.
8. Troubleshooting
8.1 Action Server Not Registering
If you see an error about action_respond_from_db not being found, restart the action server:

sh
Copy
Edit
rasa run actions
8.2 Database Not Updating
Ensure your SQLite database is updated:

sh
Copy
Edit
sqlite3 database/business_data.db
SELECT * FROM business_intents;
If there are no rows, reinitialize the database.