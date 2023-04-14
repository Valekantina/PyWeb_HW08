import pika
from mongoengine import connect, DoesNotExist
from models import Client


connect(host="mongodb+srv://vgordynska:TheLastOfUs1@goithw.euffuef.mongodb.net/?retryWrites=true&w=majority")


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue="email_queue")

    def callback(ch, method, properties, body):
        try:
            message = body.decode()
            contact = Client.objects.get(id=message)
            print(f"New email was received {message}")
            contact.sent_message = True
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except DoesNotExist:
            print(f"Email cannot be sent")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="email_queue", on_message_callback=callback)
    print("Your email is in the sending queue")
    channel.start_consuming()


if __name__ == "__main__":
    main()
