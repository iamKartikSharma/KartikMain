from flask import Blueprint, request, jsonify
import json

# Create the blueprint
kb_bp = Blueprint('knowledge_base', __name__, url_prefix='/kb')

@kb_bp.route('/', methods=['GET'])
def get_knowledge():
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