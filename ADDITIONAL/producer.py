import pika
from models import Client
from faker import Faker
from random import choice

fake = Faker("en-US")


def seed_clients(n):
    for _ in range(n):
        contact = Client(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            best_method=choice(["SMS", "Email"])
        )
        contact.save()
        print(f"New person {contact.fullname} added to the contact list")


def send_messages():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue="email_queue")
    channel.queue_declare(queue="sms_queue")

    contacts = Client.objects()
    for contact in contacts:
        message = str(contact.id)
        if contact.best_method == "SMS":
            channel.basic_publish(
                exchange="", routing_key="sms_queue", body=message)
            print(f"Your sms-message was sent to {contact.fullname}")
        elif contact.best_method == "Email":
            channel.basic_publish(
                exchange="", routing_key="email_queue", body=message)
            print(f"Your email was sent to {contact.fullname}")

    connection.close()


if __name__ == "__main__":
    send_messages()
