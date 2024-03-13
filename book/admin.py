from django.contrib import admin, messages
from django.db.models import Avg

from book.models import *


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'genre', 'publication_date', 'average_rating']

    def average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

    average_rating.short_description = 'Средний рейтинг'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not (1 <= obj.rating <= 5):
            return messages.error(request,'Рейтинг должен быть в диапазоне от 1 до 5.')
        existing_reviews = Review.objects.filter(book=obj.book, user=obj.user)
        if existing_reviews.exists():
            return messages.error(request, 'Отзыв от данного пользователя для данной книги уже существует.')

        super().save_model(request, obj, form, change)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass
