from mongoengine import connect, Document, StringField, BooleanField

connect(host="mongodb+srv://vgordynska:TheLastOfUs1@goithw.euffuef.mongodb.net/?retryWrites=true&w=majority")


class Client(Document):
    fullname = StringField(required=True)
    email = StringField()
    phone = StringField()
    address = StringField()
    sent_message = BooleanField()
    best_method = StringField()
