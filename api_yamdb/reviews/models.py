from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.title}: {self.author}"

class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.review}: {self.author}"

