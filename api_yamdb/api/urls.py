from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import signup

urlpatterns = [
    path(
        'auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'auth/signup/', signup, name='signup'
    )
]
