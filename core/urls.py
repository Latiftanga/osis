from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from core import views


app_name = 'core'

urlpatterns = [
    path('', views.api_root),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('auth-token/', obtain_jwt_token),
    path('auth-token/refresh/', refresh_jwt_token, name='token_refresh'),
    # path('create/', views.UserCreateAPIView.as_view(), name='create-user'),
    # path('token/', views.CreateTokenAPIView.as_view(), name='get-token'),
    # path('me/', views.ManageUserView.as_view(), name='user-profile'),
]
