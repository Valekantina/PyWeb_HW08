import redis
from redis_lru import RedisLRU
from mongoengine import DoesNotExist
from models import Quotes, Author

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def find_name(name: str):
    try:
        author = Author.objects(fullname__startswith=name.title()).first()
        quotes = Quotes.objects(author=author)
        result = [
            f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(f"Author {name.title()} was not found within the database")


@cache
def find_one_tag(tag: str):
    try:
        quotes = Quotes.objects(tags__startswith=tag.lower())
        result = [
            f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(f"Tag {tag.lower()} was not found in the database")


@cache
def find_tags(tags: list):
    try:
        quotes = Quotes.objects(tags__in=tags)
        result = [
            f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(
            f"Tags {str([tag.lower() for tag in tags])} do not exist in database")


if __name__ == "__main__":
    while True:
        text = input("Enter command: ")
        if text.lower() == "exit":
            print("Goodbye!")
            break
        try:
            input_text = text.split(".")
            command = input_text[0]
            data = input_text[1].strip().split(",")
            if len(data) <= 1:
                data = data[0]
            match command:
                case "name":
                    find_name(data)
                case "tag":
                    find_one_tag(data)
                case "tags":
                    find_tags(data)
                case _:
                    print("Unknown command")
        except Exception as err:
            print(f"Error {err}")
