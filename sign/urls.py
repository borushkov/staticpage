from sign import views
from django.urls import path
from .views import signup, signup2, login_view, login2, logout_view

urlpatterns = [
    # Вход (2 шага)
    path('login/', login_view, name='login'),      # Шаг 1: email/username
    path('login2/', login2, name='login2'),        # Шаг 2: пароль
    
    # Выход
    path('logout/', logout_view, name='logout'),
    
    # Профиль
    path('profile/', views.profile, name='profile'),
    path('my-posts/', views.my_posts, name='my_posts'),
    
    # Регистрация (2 шага)
    path('signup/', signup, name='signup'),        # Шаг 1: email
    path('signup2/', signup2, name='signup2'),     # Шаг 2: username + пароль
]