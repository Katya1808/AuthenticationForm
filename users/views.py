from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout


def home_view(request):
    return render(request, template_name='home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Форма сама покажет ошибку "Неверный логин или пароль"
                pass
    else:
        form = AuthenticationForm()

    return render(request, template_name='login.html', context={'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # Создаём пользователя

            # ⚠️ ВАЖНО: в UserCreationForm пароль лежит в поле password1
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, template_name='signin.html', context={'form': form})


def logout_view(request):
    logout(request)  #
    return redirect('home')
