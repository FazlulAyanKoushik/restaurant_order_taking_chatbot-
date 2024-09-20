"""
    This file contains helper functions that are used to interact with the database.
"""

import random
import string
from datetime import datetime

from models import (
    Contacts,
    Message_db,
)


def insert_into_contacts(name, whatsapp):
    contact = Contacts(
        name=name,
        whatsapp=whatsapp,
        created_at=datetime.now()
    )
    contact.save()


def insert_into_message(user_number, message, user_type):
    new_msg = Message_db(
        user_number=user_number,
        message=message,
        user_type=user_type,
        created_at=datetime.now()
    )
    new_msg.save()


def generate_random_string(length):
    characters = string.digits  # Include only digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
