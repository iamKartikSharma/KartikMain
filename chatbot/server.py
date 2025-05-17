from flask import Blueprint, request, jsonify, render_template, send_from_directory
import os
import json
import time
from datetime import datetime
from config import KNOWLEDGE_BASE_KEY, AGENT_KEY

# Create the blueprint
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api')

# Session storage (in production, use a database)
sessions = {}

@chatbot_bp.route('/chat', methods=['POST'])
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
        response = "Hello! Welcome to Barbeque Nation. I'm your virtual assistant and I'm here to help you with reservations, menu questions, and more. How can I assist you today?"
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
    
    # Import the knowledge base response function
    from knowledge_base.data import get_knowledge_base_response
    
    # Try to get a response from the knowledge base using environment variables
    kb_response = get_knowledge_base_response(message, KNOWLEDGE_BASE_KEY, AGENT_KEY)
    
    if kb_response:
        response = kb_response
    else:
        # Fallback response if knowledge base doesn't have an answer
        response = "I don't have specific information about that. Would you like to know about our menu, locations, or make a reservation?"
    
    # Update session history with bot response
    session['history'][-1]['bot'] = response
    
    return jsonify({'response': response, 'state': 'response'})