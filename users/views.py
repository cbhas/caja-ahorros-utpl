from django.contrib.auth import login, authenticate, logout
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserForm
from wallets.models import Wallet
from django.db import transaction  # Añade esta línea al inicio con las otras importaciones

def login_required_custom(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap

def login_view(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')

    return render(request, 'users/login.html')


@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Asegura que tanto el usuario como la wallet se creen o ninguno
                # Crear y guardar el usuario
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                # Verificar si el usuario ya tiene un wallet antes de crear uno nuevo
                if not Wallet.objects.filter(user=user).exists():
                    Wallet.objects.create(user=user, balance=0)

                messages.success(request, 'Cuenta y wallet creadas exitosamente.')
                return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = CustomUserForm()

    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
