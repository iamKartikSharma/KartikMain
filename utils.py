import json
import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def tokenize(text):
    """
    Split text into tokens and return token count.
    
    Args:
        text (str): Text to tokenize
        
    Returns:
        int: Number of tokens
    """
    return len(word_tokenize(text))

def transition_state(current_state, user_input, context=None):
    """
    Determine the next state based on current state and user input.
    
    Args:
        current_state (str): Current conversation state
        user_input (str): User's message
        context (dict): Conversation context
        
    Returns:
        tuple: (next_state, intent)
    """
    if context is None:
        context = {}
    
    user_input = user_input.lower()
    
    # Define keywords for intent detection
    booking_keywords = ['book', 'reservation', 'reserve', 'table', 'seat', 'dinner', 'lunch']
    cancel_keywords = ['cancel', 'reschedule', 'change reservation']
    faq_keywords = ['hour', 'open', 'menu', 'price', 'cost', 'location', 'address', 'buffet', 'veg', 'non-veg']
    goodbye_keywords = ['bye', 'goodbye', 'thank', 'thanks', 'exit', 'quit', 'end']
    
    # Check for goodbye intent in any state
    if any(keyword in user_input for keyword in goodbye_keywords):
        return 'goodbye', 'goodbye'
    
    # State transitions
    if current_state == 'greeting':
        # From greeting, go to intent detection
        return 'intent_detection', None
        
    elif current_state == 'intent_detection':
        # Detect intent from user input
        if any(keyword in user_input for keyword in booking_keywords):
            return 'booking', 'booking'
        elif any(keyword in user_input for keyword in cancel_keywords):
            return 'cancellation', 'cancellation'
        elif any(keyword in user_input for keyword in faq_keywords):
            return 'faq', 'faq'
        else:
            return 'fallback', None
            
    elif current_state == 'booking':
        # Handle booking flow
        if 'date' not in context and ('today' in user_input or 'tomorrow' in user_input or re.search(r'\d{1,2}[/-]\d{1,2}', user_input)):
            # User provided a date
            return 'booking', 'booking_date'
        elif 'time' not in context and re.search(r'\d{1,2}(?::\d{2})?\s*(?:am|pm)', user_input):
            # User provided a time
            return 'booking', 'booking_time'
        elif 'guests' not in context and re.search(r'\d+\s*(?:people|persons|guests)', user_input):
            # User provided number of guests
            return 'booking', 'booking_guests'
        elif 'confirmation' not in context and ('yes' in user_input or 'confirm' in user_input):
            # User confirmed booking
            return 'booking_confirmation', 'booking_confirmed'
        else:
            return 'booking', 'booking'
            
    elif current_state == 'cancellation':
        if 'booking_id' not in context and re.search(r'[A-Z0-9]{6,}', user_input):
            # User provided booking ID
            return 'cancellation_confirmation', 'cancellation_confirmed'
        else:
            return 'cancellation', 'cancellation'
            
    elif current_state == 'faq':
        # Stay in FAQ state for follow-up questions
        return 'faq', 'faq'
        
    elif current_state == 'fallback':
        # From fallback, try to detect intent again
        if any(keyword in user_input for keyword in booking_keywords):
            return 'booking', 'booking'
        elif any(keyword in user_input for keyword in cancel_keywords):
            return 'cancellation', 'cancellation'
        elif any(keyword in user_input for keyword in faq_keywords):
            return 'faq', 'faq'
        else:
            return 'fallback', None
            
    elif current_state == 'booking_confirmation' or current_state == 'cancellation_confirmation':
        # After confirmation, go to goodbye
        return 'goodbye', 'goodbye'
        
    # Default: stay in current state
    return current_state, None

def get_kb_response(city, intent, query):
    """
    Get a response from the knowledge base.
    
    Args:
        city (str): City name
        intent (str): Intent type
        query (str): User query
        
    Returns:
        str: Response from knowledge base or None if not found
    """
    try:
        # Load the appropriate knowledge base file
        kb_file = f'kb_data/{city.lower()}_kb.json'
        with open(kb_file, 'r') as f:
            kb_data = json.load(f)
        
        if intent not in kb_data:
            return None
        
        # Convert query to lowercase for matching
        query = query.lower()
        
        # Search for matching FAQ
        for item in kb_data[intent]:
            # Check if any keywords from the question match the query
            question = item.get('question', '').lower()
            keywords = question.split()
            
            # Count matching keywords
            matches = sum(1 for keyword in keywords if keyword in query)
            
            # If more than 2 keywords match or exact phrase match, return the answer
            if matches >= 2 or question in query:
                return item.get('answer')
        
        # No match found
        return None
        
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def chunk_text(text, max_tokens=800):
    """
    Split text into chunks of maximum token size.
    
    Args:
        text (str): Text to split
        max_tokens (int): Maximum tokens per chunk
        
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    for word in words:
        # Approximate token count (words are usually 1-2 tokens)
        word_tokens = len(word) // 4 + 1
        
        if current_token_count + word_tokens <= max_tokens:
            current_chunk.append(word)
            current_token_count += word_tokens
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_token_count = word_tokens
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks