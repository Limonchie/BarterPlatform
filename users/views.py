from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                Profile.objects.create(user=user)
            except Exception as e:
                messages.error(request, f"Ошибка создания профиля: {e}")
                return redirect('register')
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('ad_list')
        else:
            # Вывод ошибок валидации
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ad_list')
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'form': form})
