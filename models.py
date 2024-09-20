from mongoengine import Document, SequenceField, StringField, DateTimeField


class Contacts(Document):
    _id = SequenceField(Primary_key=True)
    name = StringField()
    whatsapp = StringField()
    created_at = DateTimeField()


class Message_db(Document):
    _id = SequenceField(primary_key=True)
    user_number = StringField()
    message = StringField()
    user_type = StringField()
    created_at = DateTimeField()
