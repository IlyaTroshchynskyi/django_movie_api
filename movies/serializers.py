"""
    Collect all serializers for movie api
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Movie, Category, Review, Rating, Actor, Genre, UserWishes, \
    RatingStar, Director
from .tasks import send_notification_email


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for all CRUD operations for category view
    """

    class Meta:

        model = Category
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for all CRUD operations for actor view
    """

    class Meta:
        model = Actor
        fields = ('id', 'name', 'age', 'description')


class DirectorSerializer(serializers.ModelSerializer):
    """
    Serializer for all CRUD operations for director view
    """

    class Meta:

        model = Director
        fields = ('id', 'name', 'age')


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for all CRUD operations for genre view
    """

    class Meta:
        model = Genre
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):

    rating_user = serializers.BooleanField(read_only=True)
    middle_star = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'year', 'country', 'directors',
                  'actors', 'genres', 'world_premier', 'budget', 'fees_is_usa',
                  'fees_in_world', 'category', 'rating_user', 'middle_star',
                  'url')

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        list_films = UserWishes.objects.filter(movie=instance.id)
        json_data = WishesSerializer(list_films, many=True).data
        send_notification_email.delay(json_data)
        return instance


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users review
    """

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """
    Filter for reviews. Will be present only parents
    """

    def to_representation(self, data):
        """
        Filter query set where parent=None
        :param data: Queryset
        :return:
        """
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    Output recursively children
    """

    def to_representation(self, instance):
        """
        :param instance: Movie object from db.
        self.parent = RecursiveSerializer
        self.parent.parent = ReviewSerializer
        :return: OrderedDict
        """

        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for reviews
    """
    children = RecursiveSerializer(many=True)

    class Meta:
        """
        FilterReviewListSerializer You want to provide particular validation of
        the lists, such as checking that one element does not conflict with
        another element in a list.
        """
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('id', 'name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for film detail
    """
    category = CategorySerializer()
    directors = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CreateRatingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating rating for films
    """
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        """
        Create or update the object to the database.
        :param validated_data: OrderedDict
        :return: Rating
        """
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for ratings
    """
    class Meta:
        model = RatingStar
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class WishesSerializer(serializers.ModelSerializer):
    """
    Serializer for user wishes
    """

    user = UserSerializer()
    movie = MovieListSerializer()
    added = serializers.DateField(read_only=True)

    class Meta:
        model = UserWishes
        fields = ('id', 'movie', 'user', 'added')


class WishesCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating ratings for movie
    """

    class Meta:
        model = UserWishes
        fields = ('movie', )

    def create(self, validated_data):
        """
        Create the object to the database.
        :param validated_data: OrderedDict
        :return: UserWishes
        """
        wishes = UserWishes.objects.create(
            user=validated_data.get('user', None),
            movie=validated_data.get('movie', None)
        )
        return wishes
