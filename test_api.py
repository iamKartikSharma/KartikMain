import requests
import json

def test_chat_api():
    """Test the chat API endpoint."""
    url = "http://localhost:5000/api/chat"
    
    # Test data
    payload = {
        "message": "What are the opening hours in Delhi?",
        "session_id": "test_session_123",
        "knowledge_base_key": "knowledge_base_b1b78548599a518d",
        "agent_key": "agent_ecc994045a6f926726cb433bfd"
    }
    
    # Send request
    response = requests.post(url, json=payload)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    test_chat_api()