import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from ...models import Book, Author, Language, Category
from django.core.files import File
from dotenv import load_dotenv
from envparse import Env

load_dotenv()
env = Env()

class Command(BaseCommand):
    help = 'Generate random books'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of books to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        User = get_user_model()
        superuser = User.objects.get(username='admin')

        for _ in range(count):
            author = Author.objects.create(name=fake.name(), bio=fake.text())
            language_name = fake.language_name()
            language, created = Language.objects.get_or_create(name=language_name)
            category = Category.objects.create(name=fake.word())
            title = fake.sentence()
            description = fake.paragraph()
            publication_date = fake.date()
            price = fake.random_int(min=10, max=100)
            quantity_in_stock = fake.random_int(min=0, max=100)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cover_image_path = os.path.join(base_dir, env.str('BOOK_IMAGE_PATH'))

            book = Book(
                title=title,
                description=description,
                author=author,
                language=language,
                category=category,
                publication_date=publication_date,
                price=price,
                quantity_in_stock=quantity_in_stock,
                cover_image=cover_image_path,
                is_visible=True,
            )
            book.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} books'))

