import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Loads data from CSV files into the database'
    CSV_DIR = './static/data/'
    CSV_FILES = {'category': Category,
                 'genre': Genre,
                 'users': User,
                 'titles': Title,
                 'review': Review,
                 'comments': Comment,
                 'genre_title': Title.genre.through}

    def handle(self, *args, **options):
        self.run()

    def run(self):
        #self.load_users()
        self.load_categories()
        #self.load_genres()
        #self.load_titles()
        #self.load_reviews()
        #self.load_comments()
        #self.load_title_genres()

    def load_categories(self):
        for file, models in self.CSV_FILES.items():
            model = models
            with open(self.CSV_DIR + file + '.csv',
                      encoding='utf8',
                      newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    obj = model(**row)
                    obj.save()

    '''def load_genres(self):
        with open(self.CSV_DIR + '/genre.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre = Genre(id=row['id'],
                              name=row['name'],
                              slug=row['slug'],)
                genre.save()

    def load_titles(self):
        with open(CSV_DIR + '/titles.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title(id=row['id'],
                              name=row['name'],
                              year=row['year'],
                              category_id=row['category'])
                title.save()

    def load_reviews(self):
        with open(CSV_DIR + '/review.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Review(id=row['id'],
                                title_id=row['title_id'],
                                text=row['text'],
                                author_id=row['author'],
                                score=row['score'],
                                pub_date=row['pub_date'])
                review.save()

    def load_comments(self):
        with open(CSV_DIR + '/comments.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comment = Comment(id=row['id'],
                                  review_id=row['review_id'],
                                  text=row['text'],
                                  author_id=row['author'],
                                  pub_date=row['pub_date'])
                comment.save()

    def load_users(self):
        with open(CSV_DIR + '/users.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = User(id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                data.save()

    def load_title_genres(self):
        with open(CSV_DIR + '/genre_title.csv',
                  encoding='utf8',
                  newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                data = Title.genre.through.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],)
                print(data)'''
