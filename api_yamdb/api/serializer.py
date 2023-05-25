from review.models import Category, Review, Comment, Genre, Title
from rest_framework import serializers


class CategorySerializer(serialiser.ModelSerializer):
    class Meta:
        fields = ('name','slug') 
        model = Category

class GenreSerializer(serialiser.ModelSerializer):
    class Meta:
        fields = ('name','slug')
        model = Genre
        
class TitleSerializer(serialiser.ModelSerializer):
    rating = serializer.SerializerMethodField()
    genre = GenreSerializer(required=False, many=True)
    category = CategorySerializer(required=False)
    
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
    
    def get_rating(self, instance):
        return instance.
    

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          required=False,
                                          default=serializers.
                                          CurrentUserDefault())
    title = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'author', 'pub_date')

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
        read_only_fields = ('author',)