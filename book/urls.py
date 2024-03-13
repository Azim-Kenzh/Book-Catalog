
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from book.views import HomeViewSetList, BookViewSetDetail, FavoriteViewSet

router = DefaultRouter()
router.register('home', HomeViewSetList)
router.register('book-detail', BookViewSetDetail)
router.register('favorite', FavoriteViewSet)

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
