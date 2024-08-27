from mongoengine import Document, StringField, BooleanField, URLField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField

class Post(EmbeddedDocument):
    # Define the schema for a post here
    # Example fields:
    title = StringField(required=True)
    content = StringField()
    timestamp = StringField()

class Profile(Document):
    id = StringField(primary_key=True)
    name = StringField(required=True)
    nickName = StringField()
    verified = BooleanField(default=False)
    signature = StringField()
    avatar = URLField()
    avatarCaption = StringField()
    privateAccount = BooleanField(default=False)
    region = StringField(default="US")
    following = IntField(default=0)
    friends = IntField(default=0)
    fans = IntField(default=0)
    heart = IntField(default=0)
    video = IntField(default=0)
    posts = ListField(EmbeddedDocumentField(Post))