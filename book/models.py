from pyexpat.errors import messages

from django.db import models

from account.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    publication_date = models.DateField(verbose_name='Дата публикации')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name='Книга')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Отзыв')

    def __str__(self):
        return f"Отзыв на книгу '{self.book.title}' от {self.user.email}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user.email} - {self.book.title}'

    def save(self, *args, **kwargs):
        existing_favorites = Favorite.objects.filter(user=self.user, book=self.book)
        if existing_favorites.exists():
            return
        super().save(*args, **kwargs)
