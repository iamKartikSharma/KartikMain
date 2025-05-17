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
├── app.py
├── config.py
├── post_call_logger.py
├── server.py
├── test_api.py
├── utils.pys
│
├── chatbot/ 
├── kb_data/
├── knowledge_base/
├── state_prompts/
├── static/ 
├── templates/
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
