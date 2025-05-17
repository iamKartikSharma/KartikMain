{% if intent == 'booking_date' %}
Great! I've noted down the date. Could you please tell me what time you'd like to book the table for?
{% elif intent == 'booking_time' %}
Perfect! And how many people will be dining?
{% elif intent == 'booking_guests' %}
Excellent! For which Barbeque Nation location would you like to make this reservation? We have multiple outlets in Delhi and Bangalore.
{% else %}
I'd be happy to help you book a table at Barbeque Nation. Could you please provide the following details:
1. Which date would you like to visit?
2. What time would you prefer?
3. How many people will be dining?
4. Which city and location?
{% endif %}
I'd be happy to help you with that. Could you please provide more details about what you're looking for? For example, are you interested in booking a table, cancelling a reservation, or do you have questions about our menu or locations?