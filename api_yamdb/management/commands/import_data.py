import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from reviews.models import Category, Genre, Title

class Command(BaseCommand):
    help = 'Imports data from CSV files into the database'

    def handle(self, *args, **options):
        categories_file = 'static/data/categories.csv'
        genres_file = 'static/data/genres.csv'
        titles_file = ' static/data/titles.csv'

        self.import_categories(categories_file)
        self.import_genres(genres_file)
        self.import_titles(titles_file)

    def import_categories(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name = row[0]
                category = Category(name=name)
                category.save()

    def import_genres(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name = row[0]
                genre = Genre(name=name)
                genre.save()

    def import_titles(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name = row[0]
                category_name = row[1]
                genre_names = row[2:]

                category = Category.objects.get(name=category_name)
                genres = Genre.objects.filter(name__in=genre_names)

                title = Title(name=name, category=category)
                title.save()
                title.genre.set(genres)
