from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente. Ya puedes iniciar sesión.')
            return redirect('login')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'ferreteria/registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'ferreteria/login.html')

@login_required
def vista_inicio(request):
    return render(request, 'ferreteria/inicio.html', {'usuario': request.user})