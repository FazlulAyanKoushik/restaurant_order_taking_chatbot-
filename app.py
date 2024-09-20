from datetime import timedelta, datetime

from flask import Flask, request, session
from flask_session import Session
# from link_training import save_to_docx
from mongoengine import *
from twilio.rest import Client

from gpt_functions import *
from helpers import (
    insert_into_contacts,
    insert_into_message,
)
from models import (
    Contacts,
)

# from bot_send_mail import send_otp_message, send_new_user_message, send_forgot_pass_message
# from tasks import later_process_files
# from write_excel import search_yachts
load_dotenv()

openAI_key = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=openAI_key)

ASSISTANT_ID = "asst_nPJUQiVUwjpuL8ZF6c4jPsS6"

app = Flask(__name__)
app.config['secret_key'] = '5800d5d9e4405020d527f0587538abbe'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
phone_number = os.getenv('PHONE_NUMBER')
messaging_sid = os.getenv('MESSAGING_SID')
twilio_client = Client(account_sid, auth_token)

connect('restaurant_bot_db', host=os.getenv('MONGO_URI'))


@app.route('/whatsapp', methods=['POST'])
def handle_incoming_message():
    message = request.form.get('Body')  # the message of sender
    sender = request.form.get('From')  # the sender's phone number "whatsapp:+2348123456789"
    profile_name = request.form.get('ProfileName')  # the name of the sender
    media_url = request.form.get('MediaUrl0')  # the media url of the sender

    user = Contacts.objects(whatsapp=sender[9:]).first()
    if not user:
        insert_into_contacts(profile_name, sender[9:])
    if message is not None or message != "":
        insert_into_message(sender[9:], message, "user")

    if media_url:
        insert_into_message(sender[9:], "media_url", "user")

    if 'threads_id' not in session:
        session['thread_id'] = createThread(message)

    else:
        try:
            sendNewMessage(session.get('thread_id'), message)
        except:
            wait_msg = twilio_client.messages.create(
                from_=phone_number,
                body="Please wait for generating the previous message's response",
                to=sender
            )
            return "okay", 200

    # Trigger the assistant to run on a thread. This will start the conversation.
    run = runAssistant(session.get('thread_id'), ASSISTANT_ID)

    final_response = ""

    while True:
        run_status = checkRunStatus(session.get('thread_id'), run.id)
        print(run_status.status)

        if run_status.status == "failed":
            break

        if run_status.status == "completed":
            # Retrieve the response from an existing thread.
            final_response = retrieveResponse(session.get('thread_id'))
            break

    # Send the response to the user via WhatsApp using Twilio
    twilio_client.messages.create(
        from_=phone_number,
        body=final_response,
        to=sender
    )
    return "Okay", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
