from django.db.models import Avg
from rest_framework import serializers

from book.models import *


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для книг.

    Поля:
        url (HyperlinkedIdentityField): Гиперссылка на детали книги.
        is_favorite (BooleanField): Флаг, указывающий, добавлена ли книга в избранное.
    """

    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    is_favorite = serializers.BooleanField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        """
            Преобразует экземпляр модели в словарь для сериализации.
        """

        representation = super().to_representation(instance)
        representation['genre'] = {"id": instance.genre.id, "name": instance.genre.name}
        representation['author'] = {"id": instance.author.id, "full_name": instance.author.full_name}

        # Рассчитываем средний рейтинг книги
        representation['average_rating'] = round(instance.reviews.aggregate(Avg('rating'))['rating__avg'], 1)

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """
        Сериализатор для отзывов о книгах.
    """

    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'text')


class BookDetailSerializer(serializers.ModelSerializer):
    """
       Сериализатор для подробных данных о книгах.
   """

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        """
            Преобразует экземпляр модели в словарь для сериализации.
        """

        representation = super().to_representation(instance)
        representation['genre'] = {"id": instance.genre.id, "name": instance.genre.name}
        representation['author'] = {"id": instance.author.id, "full_name": instance.author.full_name}
        representation['average_rating'] = round(instance.reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для избранных книг.
    """

    class Meta:
        model = Favorite
        exclude = ('user',)

    def to_representation(self, instance):
        """
            Преобразует экземпляр модели в словарь для сериализации.
        """
        representation = super().to_representation(instance)
        representation['book'] = {"id": instance.book.id, "name": instance.book.title}
        return representation