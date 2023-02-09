import csv
import random
import string
import uuid


def generate_random_string(string_length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))


def generate_random_book():
    book = {
        'uuid': uuid.uuid4(),
        'title': generate_random_string(),
        'author': '1900-01-01',
        'date_published': ''.join(random.choices(string.digits, k=5)),
        'publisher': generate_random_string(),
    }
    return book


def write_books_to_csv(filename):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ["uuid", "title", "author", "date_published", "publisher"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(200):
            writer.writerow(generate_random_book())


write_books_to_csv('books1.csv')
