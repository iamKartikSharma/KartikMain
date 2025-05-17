# Barbeque Nation Chatbot

A Flask-based chatbot for Barbeque Nation restaurant that handles booking inquiries, FAQs, and more using a state machine approach and knowledge base.

## Project Overview

This chatbot uses:
- Flask for the backend API
- State machine logic for conversation flow
- Knowledge base for restaurant information
- Google Sheets integration for conversation logging
- Simple HTML/CSS/JS frontend

barbeque-nation-chatbot/
│
├── app.py # Entry point for Flask app
├── config.py # Configuration variables and environment setup
├── post_call_logger.py # For logging post-call analysis (optional)
├── server.py # Webhook server for Retell AI integration
├── test_api.py # API testing scripts
├── utils.py # Utility functions
│
├── chatbot/ # Core chatbot logic (state handling, transitions)
├── kb_data/ # Preloaded knowledge base data
├── knowledge_base/ # Knowledge base search/lookup functions
├── state_prompts/ # Prompt templates for each conversation state
├── static/ # Static frontend files (JS/CSS/images)
├── templates/ # HTML templates for web frontend
├── webhook/ # Retell webhook logic
│
├── .env.example # Sample environment variable config
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── Screenshot 2025-05-18 ...png # UI flow or architecture diagrams


![Screenshot 2025-05-18 005932](https://github.com/user-attachments/assets/72478d28-9a6d-444e-abbf-f3630ea38b64)
![Screenshot 2025-05-18 010249](https://github.com/user-attachments/assets/afe90b74-d678-485a-9f1a-c41830dcf48f)
![Screenshot 2025-05-18 010314](https://github.com/user-attachments/assets/22d87b6a-bcb3-470b-8498-43f5f95cb5bc)
