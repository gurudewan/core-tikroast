from mongoengine import Document, StringField, DateTimeField, BooleanField, DictField, connect
from datetime import datetime
from app.consts import MONGO_DB_STRING

connect('your_database', host=MONGO_DB_STRING)

class Status(Document):
    is_profile_private = BooleanField(default=False)
    profile_scraped = BooleanField(default=False)
    profile_scraped_timestamp = DateTimeField()
    is_free_analysed = BooleanField(default=False)
    free_analysed_timestamp = DateTimeField()
    posts_scraped = BooleanField(default=False)
    posts_scraped_timestamp = DateTimeField()
    paid_analysis_started = BooleanField(default=False)
    paid_analysis_timestamp = DateTimeField()

class User(Document):
    username = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    full_profile = DictField()
    analysis = DictField()
    has_paid = BooleanField(default=False)
    statuses = DictField()