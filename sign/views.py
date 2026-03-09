from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from news.models import Post
from django.contrib.auth.decorators import login_required


def signup(request):
    """Первый шаг регистрации — ввод email"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            return render(request, 'accounts/signup.html', {
                'error': 'Пожалуйста, введите email',
                'email': email
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html', {
                'error': 'Пользователь с таким email уже зарегистрирован',
                'email': email
            })
        
        request.session['pending_email'] = email
        return redirect('signup2')
    
    return render(request, 'accounts/signup.html')


def signup2(request):
    """Второй шаг регистрации — username + пароль"""
    email = request.session.get('pending_email')
    if not email:
        messages.warning(request, 'Пожалуйста, начните с первого шага регистрации')
        return redirect('signup')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = {}

        if not username:
            errors['username_error'] = "Имя пользователя обязательно"
        elif len(username) < 3:
            errors['username_error'] = "Минимум 3 символа"
        elif User.objects.filter(username=username).exists():
            errors['username_error'] = "Это имя пользователя уже занято"

        if not password1:
            errors['password_error'] = "Введите пароль"
        elif password1 != password2:
            errors['password_error'] = "Пароли не совпадают"
        elif len(password1) < 8:
            errors['password_error'] = "Пароль должен содержать минимум 8 символов"
        elif not any(c.isupper() for c in password1):
            errors['password_error'] = "Пароль должен содержать хотя бы одну заглавную букву"
        elif not any(c.islower() for c in password1):
            errors['password_error'] = "Пароль должен содержать хотя бы одну строчную букву"
        elif not any(c.isdigit() for c in password1):
            errors['password_error'] = "Пароль должен содержать хотя бы одну цифру"

        if errors:
            return render(request, 'accounts/signup2.html', {
                'email': email,
                'username': username,
                **errors
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            if 'pending_email' in request.session:
                del request.session['pending_email']

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Добро пожаловать, {user.username}! Регистрация прошла успешно.")
            return redirect('post_list')
            
        except Exception as e:
            return render(request, 'accounts/signup2.html', {
                'email': email,
                'username': username,
                'password_error': f'Ошибка при создании аккаунта: {str(e)}'
            })

    return render(request, 'accounts/signup2.html', {'email': email})


# ✅ НОВЫЙ ДВУХЭТАПНЫЙ ВХОД

def login_view(request):
    """Шаг 1 входа — ввод email или username"""
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        
        if not identifier:
            return render(request, 'accounts/login.html', {
                'error': 'Пожалуйста, введите email или имя пользователя',
                'email': identifier
            })
        
        # Проверяем существует ли пользователь
        user_exists = False
        
        # Проверка по email
        if '@' in identifier:
            user_exists = User.objects.filter(email=identifier.lower()).exists()
        else:
            # Проверка по username
            user_exists = User.objects.filter(username=identifier).exists()
        
        if not user_exists:
            return render(request, 'accounts/login.html', {
                'error': 'Пользователь не найден',
                'email': identifier
            })
        
        # Сохраняем в сессии
        request.session['login_identifier'] = identifier
        return redirect('login2')
    
    return render(request, 'accounts/login.html')


def login2(request):
    """Шаг 2 входа — ввод пароля"""
    identifier = request.session.get('login_identifier')
    
    if not identifier:
        messages.warning(request, 'Пожалуйста, начните с первого шага')
        return redirect('login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Определяем username для аутентификации
        if '@' in identifier:
            # Это email - находим username
            try:
                user_obj = User.objects.get(email=identifier.lower())
                username = user_obj.username
            except User.DoesNotExist:
                return render(request, 'accounts/login2.html', {
                    'identifier': identifier,
                    'error': 'Пользователь не найден'
                })
        else:
            # Это уже username
            username = identifier
        
        # Аутентификация
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Очищаем сессию
            if 'login_identifier' in request.session:
                del request.session['login_identifier']
            
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('post_list')
        else:
            return render(request, 'accounts/login2.html', {
                'identifier': identifier,
                'error': 'Неверный пароль'
            })
    
    return render(request, 'accounts/login2.html', {'identifier': identifier})


def logout_view(request):
    """Выход из системы"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы')
        return redirect('post_list')
    
    return render(request, 'accounts/logout.html')


@login_required
def profile(request):
    """Профиль пользователя"""
    return render(request, 'accounts/profile.html')


@login_required
def my_posts(request):
    """Мои публикации"""
    try:
        from news.models import Author
        author = Author.objects.get(user=request.user)
        posts = Post.objects.filter(author=author).order_by('-created_at')
    except:
        posts = []
    
    return render(request, 'accounts/my_posts.html', {'posts': posts})