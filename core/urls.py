from django.urls import path

from core import views


app_name = 'core'

urlpatterns = [
    path('', views.api_root),
    path('create/', views.UserCreateAPIView.as_view(), name='create-user'),
    path('token/', views.CreateTokenAPIView.as_view(), name='get-token'),
    path('me/', views.ManageUserView.as_view(), name='user-profile'),
]