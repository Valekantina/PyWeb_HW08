from mongoengine import connect, EmbeddedDocument, Document, DENY
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, ReferenceField

connect(
    host="mongodb+srv://vgordynska:TheLastOfUs1@goithw.euffuef.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    quote = StringField(required=True)
    author = ReferenceField(Author, required=True, reverse_delete_rule=DENY)
