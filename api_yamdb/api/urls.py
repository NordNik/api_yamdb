from django.urls import path

from .views import signup, token

urlpatterns = [
    path(
        'auth/token/', token, name='token'
    ),
    path(
        'auth/signup/', signup, name='signup'
    )
]
