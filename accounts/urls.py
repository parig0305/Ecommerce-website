from django.urls import path
from .views import register, user_login, user_logout, profile, change_password

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('password/', change_password, name='password_change'),
]
