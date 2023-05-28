import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class Command(BaseCommand):
    help = 'Loads data from CSV files into the database'

    def handle(self, *args, **options):
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_reviews()
        self.load_comments()

    def load_categories(self):
        with open('api_yamdb/static/data/categories.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.get_or_create(name=row['name'])

    def load_genres(self):
        with open('api_yamdb/static/data/genres.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.get_or_create(name=row['name'])

    def load_titles(self):
        with open('api_yamdb/static/data/titles.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(name=row['category'])
                title = Title.objects.create(name=row['name'], category=category)
                genres = row['genres'].split(',')
                for genre_name in genres:
                    genre = Genre.objects.get(name=genre_name.strip())
                    title.genre.add(genre)

    def load_reviews(self):
        with open('api_yamdb/static/data/reviews.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(name=row['title'])
                author = User.objects.get(username=row['author'])
                Review.objects.create(
                    text=row['text'],
                    score=int(row['score']),
                    title=title,
                    author=author
                )

    def load_comments(self):
        with open('api_yamdb/static/data/comments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Review.objects.get(id=int(row['review']))
                author = User.objects.get(username=row['author'])
                Comment.objects.create(
                    text=row['text'],
                    review=review,
                    author=author
                )
