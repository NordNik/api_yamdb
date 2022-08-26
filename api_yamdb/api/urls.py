from .views import CommentViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns =[
    path('v1/', include(v1_router.urls)),
]
