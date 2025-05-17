from flask import Flask, send_from_directory
from chatbot.server import chatbot_bp
from knowledge_base.api import kb_bp
from webhook.api import webhook_bp
import os

app = Flask(__name__)

# Register blueprints
app.register_blueprint(chatbot_bp)
app.register_blueprint(kb_bp)
app.register_blueprint(webhook_bp)

# Serve static files
@app.route('/')
def index():
    return send_from_directory('chatbot/static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('chatbot/static', path)

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test endpoint to check if API is running."""
    return jsonify({
        'status': 'success',
        'message': 'API is running correctly',
        'time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)