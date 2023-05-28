from django.core.validators import MinLengthValidator, RegexValidator
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_email, validate_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')
        model = User
        read_only_field = ('role')


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=(RegexValidator(r'^[\w.+-]+\Z'),
                    validate_email))

    username = serializers.CharField(
        required=True, max_length=150,
        validators=(
            MinLengthValidator(3),
            RegexValidator(r'^[\w.@+-]+\Z'),
            validate_username,))

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    pagination_class = PageNumberPagination

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    pagination_class = LimitOffsetPagination

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(required=False, many=True)
    category = CategorySerializer(required=False)
    pagination_class = PageNumberPagination

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title

    def get_rating(self, instance):
        return instance.reviews.aggregate(Avg('score'))['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          required=False,
                                          default=serializers.
                                          CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'author', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id'])
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на данное произведение")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          required=False,
                                          default=serializers.
                                          CurrentUserDefault())
    review = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'author', 'pub_date')
