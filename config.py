import os

# Load environment variables for API keys
KNOWLEDGE_BASE_KEY = os.environ.get('KNOWLEDGE_BASE_KEY')
AGENT_KEY = os.environ.get('AGENT_KEY')

# Validate that keys are available
if not KNOWLEDGE_BASE_KEY or not AGENT_KEY:
    print("Warning: API keys not found in environment variables.")
    # You could set default values for development, but not recommended for production