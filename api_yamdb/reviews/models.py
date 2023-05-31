from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=50)

    """'''   def save(self, *args, **kwargs):
        self.slug = slugify(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)'''"""

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=50)

    """    '''def save(self, *args, **kwargs):
        self.slug = slugify(self.name, instance=self)
        super(Genre, self).save(*args, **kwargs)'''"""

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.SmallIntegerField()
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   db_index=True,
                                   related_name='title')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='title')
    description = models.TextField(max_length=200,
                                   blank=True,
                                   null=True,)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              null=True
                              )
    text = models.TextField()

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',)
    score = models.PositiveSmallIntegerField(validators=(MaxValueValidator(10),
                                                         MinValueValidator(1)))
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return f"{self.title}: {self.author}"


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

    def __str__(self):
        return f"{self.review}: {self.author}"
