import os
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment


User = get_user_model()


class Command(BaseCommand):
    help = 'Loads data from CSV files into the database'

    def handle(self, *args, **options):
        self.run()

    def run(self):
        content = os.listdir('static/data')
        print(content)
        self.load_categories()
        '''self.load_genres()
        self.load_titles()
        self.load_reviews()
        self.load_comments()'''

    def load_categories(self):
        with open('static/data/category.csv',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            categories = []
            for row in reader:
                category = Category(id=row['id'],
                                    name=row['name'],
                                    slug=row['slug'])
                categories.append(category)
            Category.objects.bulk_create(categories)

    def load_genres(self):
        with open('static/data/genre.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.get_or_create(name=row['name'])

    def load_titles(self):
        with open('static/data/titles.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(name=row['category'])
                title = Title.objects.create(name=row['name'],
                                             category=category)
                genres = row['genres'].split(',')
                for genre_name in genres:
                    genre = Genre.objects.get(name=genre_name.strip())
                    title.genre.add(genre)

    def load_reviews(self):
        with open('static/data/review.csv', newline='') as csvfile:
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
        with open('static/data/comments.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Review.objects.get(id=int(row['review']))
                author = User.objects.get(username=row['author'])
                Comment.objects.create(
                    text=row['text'],
                    review=review,
                    author=author
                )


def run():
    cmd = Command()
    cmd.run()
