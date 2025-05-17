import requests
import json
import os
import random

def get_knowledge_base_response(query, kb_key, agent_key):
    """
    Get a response from the Retail AI knowledge base.
    
    Args:
        query (str): User query
        kb_key (str): Knowledge base key
        agent_key (str): Agent key
        
    Returns:
        str: Response from knowledge base or None if not found
    """
    try:
        # Print debug information
        print(f"Processing query: {query}")
        print(f"Using KB key: {kb_key}")
        print(f"Using agent key: {agent_key}")
        
        # API call to the Retail AI service
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {agent_key}'
        }
        
        payload = {
            'query': query,
            'kb_key': kb_key
        }
        
        try:
            # Make the API call to the knowledge base endpoint
            print("Attempting to call external API...")
            response = requests.post('https://api.retailai.com/v1/knowledge/query', 
                                    headers=headers, 
                                    json=payload,
                                    timeout=5)  # Add timeout
            
            print(f"API response status: {response.status_code}")
            
            if response.status_code == 200:
                answer = response.json().get('answer')
                print(f"Got answer from API: {answer[:50] if answer else 'None'}...")
                return answer
            else:
                print(f"API call failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
        
        # Fallback to local knowledge base if API call fails
        print("Falling back to local knowledge base")
        query = query.lower()
        
        # Load local knowledge base for testing
        try:
            kb_data = None
            if 'delhi' in query:
                print("Loading Delhi knowledge base")
                kb_file = 'kb_data/delhi_kb.json'
            else:
                print("Loading Bangalore knowledge base")
                kb_file = 'kb_data/bangalore_kb.json'
            
            # Check if file exists
            if os.path.exists(kb_file):
                with open(kb_file, 'r') as f:
                    kb_data = json.load(f)
            else:
                print(f"Knowledge base file not found: {kb_file}")
                # Provide default responses if KB files don't exist
                default_responses = {
                    'hours': "Barbeque Nation is open from 12 PM to 3:30 PM for lunch and 6:30 PM to 11 PM for dinner, seven days a week.",
                    'price': "The buffet at Barbeque Nation costs approximately ₹800 to ₹1200 per person, depending on the day and time.",
                    'location': "Barbeque Nation has multiple locations across major cities in India. Please specify which city you're interested in.",
                    'vegetarian': "Yes, Barbeque Nation offers a wide range of vegetarian options including grilled vegetables, paneer dishes, and vegetarian curries.",
                    'booking': "You can book a table at Barbeque Nation through our website, mobile app, or by calling the restaurant directly."
                }
                
                if any(word in query for word in ['hour', 'open', 'time']):
                    return default_responses['hours']
                elif any(word in query for word in ['price', 'cost', 'buffet']):
                    return default_responses['price']
                elif any(word in query for word in ['location', 'address', 'where']):
                    return default_responses['location']
                elif any(word in query for word in ['veg', 'vegetarian']):
                    return default_responses['vegetarian']
                elif any(word in query for word in ['book', 'reservation', 'table']):
                    return default_responses['booking']
                return None
                    
            # Simple keyword matching with improved detection
            answer = None
            
            # Check for hours/timing related queries
            if any(word in query for word in ['hour', 'open', 'time', 'timing', 'when']):
                answer = next((item['answer'] for item in kb_data.get('faq', []) 
                           if 'opening hours' in item['question'].lower() or 'timing' in item['question'].lower()), None)
            
            # Check for price related queries
            elif any(word in query for word in ['price', 'cost', 'buffet', 'menu', 'charge', 'fee', 'expensive']):
                answer = next((item['answer'] for item in kb_data.get('faq', []) 
                           if 'price' in item['question'].lower() or 'cost' in item['question'].lower()), None)
            
            # Check for location related queries
            elif any(word in query for word in ['location', 'address', 'where', 'place', 'situated', 'located']):
                answer = next((item['answer'] for item in kb_data.get('faq', []) 
                           if 'located' in item['question'].lower() or 'address' in item['question'].lower()), None)
            
            # Check for vegetarian related queries
            elif any(word in query for word in ['veg', 'vegetarian', 'plant', 'non-meat']):
                answer = next((item['answer'] for item in kb_data.get('faq', []) 
                           if 'vegetarian' in item['question'].lower()), None)
            
            # Check for booking related queries
            elif any(word in query for word in ['book', 'reservation', 'table', 'reserve', 'seat']):
                booking_info = next((item for item in kb_data.get('booking', []) 
                                if 'Booking Information' in item.get('info', '')), None)
                if booking_info:
                    answer = booking_info.get('details')
            
            # General greeting or hello
            elif any(word in query for word in ['hello', 'hi', 'hey', 'greetings']):
                greetings = [
                    "Hello! Welcome to Barbeque Nation. How can I assist you today?",
                    "Hi there! I'm your Barbeque Nation assistant. What information do you need?",
                    "Greetings! I'm here to help with all your Barbeque Nation queries."
                ]
                answer = random.choice(greetings)
            
            # If no specific match, try to find any relevant FAQ
            if not answer and 'faq' in kb_data:
                # Convert query to a set of words for better matching
                query_words = set(query.split())
                
                # Find FAQs with the most word matches
                best_match = None
                best_match_count = 0
                
                for item in kb_data['faq']:
                    question = item['question'].lower()
                    question_words = set(question.split())
                    match_count = len(query_words.intersection(question_words))
                    
                    if match_count > best_match_count:
                        best_match_count = match_count
                        best_match = item
                
                if best_match and best_match_count >= 1:
                    answer = best_match['answer']
            
            if answer:
                print(f"Found answer in local KB: {answer[:50]}...")
            else:
                print("No answer found in local KB")
                # Provide a fallback response
                fallback_responses = [
                    "I'm not sure I understand. Could you please rephrase your question?",
                    "I don't have specific information about that. Would you like to know about our menu, locations, or make a reservation?",
                    "I'm sorry, I don't have that information right now. Is there something else I can help you with?"
                ]
                answer = random.choice(fallback_responses)
            
            return answer
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error accessing local KB: {e}")
            # Provide a fallback response for file errors
            return "I'm having trouble accessing my knowledge base. Please try asking about our menu, locations, or making a reservation."
            
    except Exception as e:
        print(f"Error querying knowledge base: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."
