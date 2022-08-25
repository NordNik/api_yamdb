from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import GenresViewSet, CategoriesViewSet, TitlesViewSet


v1_router = SimpleRouter()
v1_router.register('genres', GenresViewSet)
v1_router.register('categories', CategoriesViewSet)
v1_router.register('titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls))
]
