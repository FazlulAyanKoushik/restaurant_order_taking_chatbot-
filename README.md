## A WhatsApp Chatbot project using Flask for taking restaurant orders.

## Technologies Used
- Python
- Flask
- Twilio API
- openai API

<hr>

clone the repository
```bash
git clone https://github.com/FazlulAyanKoushik/restaurant_order_taking_chatbot-.git
```

Create a virtual environment
```bash
pip install virtualenv
```
```bash
virtualenv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```


Install the required libraries
```bash
pip install -r requirements.txt
```

Create a .env file and add the following
```bash
OPENAI_KEY="Your openai key"
ACCOUNT_SID="Your twilio account sid"
AUTH_TOKEN="Your twilio auth token"
MESSAGING_SID="Your twilio messaging service sid"
PHONE_NUMBER="whatsapp:+14155238886"
MONGO_URI="mongodb://localhost:27017/<your_db_name>"
```

Run the application
```bash
python app.py
```