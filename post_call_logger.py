import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

class PostCallLogger:
    def __init__(self, credentials_path, spreadsheet_id):
        """
        Initialize the PostCallLogger with Google Sheets credentials.
        
        Args:
            credentials_path (str): Path to the Google service account JSON file
            spreadsheet_id (str): ID of the Google Spreadsheet to log data to
        """
        self.spreadsheet_id = spreadsheet_id
        
        # Load credentials
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=self.credentials)
            self.sheet = self.service.spreadsheets()
        except Exception as e:
            print(f"Error initializing Google Sheets API: {e}")
            self.service = None
    
    def log_conversation(self, session_id, user_query, bot_response, intent, city=None, duration=None):
        """
        Log a conversation to Google Sheets.
        
        Args:
            session_id (str): Unique session identifier
            user_query (str): The user's last query
            bot_response (str): The bot's last response
            intent (str): Detected intent (booking, faq, etc.)
            city (str, optional): City if applicable
            duration (int, optional): Duration of conversation in seconds
        
        Returns:
            bool: True if logging was successful, False otherwise
        """
        if not self.service:
            print("Google Sheets service not initialized")
            return False
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare row data
        row_data = [
            timestamp,
            session_id,
            user_query,
            bot_response,
            intent,
            city if city else "N/A",
            duration if duration else 0
        ]
        
        try:
            # Append row to the sheet
            result = self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1!A:G',  # Adjust range as needed
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [row_data]}
            ).execute()
            
            print(f"Logged conversation to Google Sheets: {result.get('updates').get('updatedCells')} cells updated")
            return True
        except Exception as e:
            print(f"Error logging to Google Sheets: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # This is just for testing - in production, these would be loaded from environment variables
    CREDENTIALS_PATH = "path/to/your/credentials.json"
    SPREADSHEET_ID = "your-spreadsheet-id"
    
    logger = PostCallLogger(CREDENTIALS_PATH, SPREADSHEET_ID)
    
    # Test logging
    logger.log_conversation(
        session_id="test123",
        user_query="Can I book a table for 4 people?",
        bot_response="Yes, I can help you book a table. What date and time would you prefer?",
        intent="booking",
        city="Delhi",
        duration=30
    )