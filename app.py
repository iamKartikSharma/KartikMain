import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
from utils import transition_state, get_kb_response, tokenize
from post_call_logger import PostCallLogger

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
GOOGLE_SHEETS_CREDENTIALS = os.environ.get('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')
GOOGLE_SHEETS_ID = os.environ.get('GOOGLE_SHEETS_ID', '')

# Initialize logger
logger = PostCallLogger(GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEETS_ID)

# Initialize Jinja environment for state prompts
jinja_env = Environment(loader=FileSystemLoader('state_prompts'))

# Session storage (in production, use a database)
sessions = {}

@app.route('/')
def index():
    """Render the chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages from the user."""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', '')
    
    # Initialize session if it doesn't exist
    if session_id not in sessions:
        sessions[session_id] = {
            'state': 'greeting',
            'context': {},
            'start_time': time.time(),
            'history': []
        }
    
    session = sessions[session_id]
    
    # If this is the first message (empty), return greeting
    if not message:
        template = jinja_env.get_template('greeting.j2')
        response = template.render()
        session['history'].append({
            'user': '',
            'bot': response,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify({'response': response, 'state': session['state']})
    
    # Add user message to history
    session['history'].append({
        'user': message,
        'bot': '',
        'timestamp': datetime.now().isoformat()
    })
    
    # Determine next state based on current state and user input
    next_state, intent = transition_state(session['state'], message, session['context'])
    session['state'] = next_state
    
    # Get city from context or try to extract from message
    city = session['context'].get('city')
    if not city and ('delhi' in message.lower() or 'new delhi' in message.lower()):
        city = 'Delhi'
        session['context']['city'] = city
    elif not city and 'bangalore' in message.lower():
        city = 'Bangalore'
        session['context']['city'] = city
    
    # Get response based on state
    if next_state == 'faq' and city:
        # Get response from knowledge base
        kb_response = get_kb_response(city, 'faq', message)
        if kb_response:
            response = kb_response
        else:
            template = jinja_env.get_template('fallback.j2')
            response = template.render(query=message)
    else:
        # Get response from state template
        template = jinja_env.get_template(f'{next_state}.j2')
        response = template.render(
            user_message=message,
            context=session['context'],
            intent=intent
        )
    
    # Update session history with bot response
    session['history'][-1]['bot'] = response
    
    # Log the conversation if it's a significant state change
    if next_state in ['booking', 'cancellation', 'goodbye']:
        duration = int(time.time() - session['start_time'])
        logger.log_conversation(
            session_id=session_id,
            user_query=message,
            bot_response=response,
            intent=intent or next_state,
            city=city,
            duration=duration
        )
    
    return jsonify({'response': response, 'state': next_state})

@app.route('/kb', methods=['GET'])
def knowledge_base():
    """Retrieve information from the knowledge base."""
    city = request.args.get('city')
    intent = request.args.get('intent')
    
    if not city or not intent:
        return jsonify({'error': 'Missing parameters. Required: city, intent'}), 400
    
    try:
        # Load the appropriate knowledge base file
        kb_file = f'kb_data/{city.lower()}_kb.json'
        with open(kb_file, 'r') as f:
            kb_data = json.load(f)
        
        # Return the relevant section
        if intent in kb_data:
            return jsonify({'data': kb_data[intent]})
        else:
            return jsonify({'error': f'Intent {intent} not found in knowledge base'}), 404
    
    except FileNotFoundError:
        return jsonify({'error': f'Knowledge base for {city} not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid knowledge base format'}), 500

@app.route('/log_call', methods=['POST'])
def log_call():
    """Log conversation data to Google Sheets."""
    data = request.json
    
    # Validate required fields
    required_fields = ['session_id', 'user_query', 'bot_response', 'intent']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Log to Google Sheets
    success = logger.log_conversation(
        session_id=data['session_id'],
        user_query=data['user_query'],
        bot_response=data['bot_response'],
        intent=data['intent'],
        city=data.get('city'),
        duration=data.get('duration')
    )
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to log conversation'}), 500

if __name__ == '__main__':
    app.run(debug=True)