from datetime import datetime
from django.db import models
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from book.models import Book, Favorite
from book.serializers import BookSerializer, BookDetailSerializer, FavoriteSerializer


class HomeViewSetList(mixins.ListModelMixin, GenericViewSet):
    """
    Представление для получения списка книг с учетом фильтров и информации о добавлении книги в избранное.

    Пример запроса:
    /api/books/home/?genre_id=1&author_id=1&start_date=1967-01-01&end_date=1972-12-31
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Возвращает список книг с учетом фильтров и информации о том, добавлена ли книга в избранное для текущего пользователя.

        Параметры запроса:
        - genre_id: идентификатор жанра для фильтрации книг по жанру
        - author_id: идентификатор автора для фильтрации книг по автору
        - start_date: начальная дата публикации для фильтрации книг по дате публикации
        - end_date: конечная дата публикации для фильтрации книг по дате публикации

        Пример запроса:
        /api/books/home/?genre_id=1&author_id=2&start_date=2022-01-01&end_date=2024-12-31
        """
        queryset = super().get_queryset()
        user = self.request.user

        # Если пользователь аутентифицирован, проверяем, добавлена ли книга в избранное для этого пользователя
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorite=models.Exists(Favorite.objects.filter(book=models.OuterRef('pk'), user=user)))

        # Получаем параметры запроса
        genre_id = self.request.query_params.get('genre_id')
        author_id = self.request.query_params.get('author_id')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        # Фильтрация по жанрам
        if genre_id:
            queryset = queryset.filter(genre__id__in=genre_id)

        # Фильтрация по авторам
        if author_id:
            queryset = queryset.filter(author__id__in=author_id)

        # Фильтрация по дате публикации
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            queryset = queryset.filter(publication_date__range=(start_date, end_date))

        return queryset


class FavoriteViewSet(viewsets.ViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Добавляет книгу в избранное для текущего пользователя.

        Параметры запроса:
        - book_id: идентификатор книги, которую необходимо добавить в избранное

        Пример запроса:
        POST /api/books/favorite/
        {
            "book_id": 1
        }
        """
        user = request.user
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Не указан ID книги'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Книга с указанным ID не найдена'}, status=status.HTTP_404_NOT_FOUND)
        favorite, created = Favorite.objects.get_or_create(user=user, book=book)
        if not created:
            return Response({'error': 'Книга уже добавлена в избранное'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Удаляет книгу из избранного для текущего пользователя.

        Параметры запроса:
        - pk: идентификатор книги, которую необходимо удалить из избранного

        Пример запроса:
        DELETE /api/books/favorite/<book_id>/
        """
        user = request.user
        try:
            favorite = Favorite.objects.get(user=user, book=pk)
        except Favorite.DoesNotExist:
            return Response({'error': 'Эта книга не находится в избранном'}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """
        Возвращает список избранных книг для текущего пользователя.
        """
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = self.serializer_class(favorites, many=True)
        return Response(serializer.data)


class BookViewSetDetail(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
