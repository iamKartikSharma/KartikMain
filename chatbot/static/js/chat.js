document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Generate a random session ID for this chat session
    const sessionId = 'session_' + Math.random().toString(36).substring(2, 15);
    
    // Function to add a message to the chat
    function addMessage(message, isUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to send a message to the server
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add the user message to the chat
        addMessage(message, true);
        
        // Clear the input field
        userInput.value = '';
        
        // Send the message to the API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
                // Keys are now handled on the server side
            })
        })
        .then(response => response.json())
        .then(data => {
            // Add the bot response to the chat
            addMessage(data.response, false);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request.', false);
        });
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Send a greeting message to initialize the chat
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: '',
            session_id: sessionId
            // Keys are now handled on the server side
        })
    })
    .then(response => response.json())
    .then(data => {
        // Add the initial greeting from the bot
        addMessage(data.response, false);
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Sorry, there was an error connecting to the server.', false);
    });
});