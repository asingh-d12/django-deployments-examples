from django.urls import path
from basic_password_auth_app import views

app_name = 'basic_password_auth_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login')
]