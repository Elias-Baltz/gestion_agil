from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import ProductoForm
from .models import Producto
from django.contrib.auth import logout

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

def es_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(es_admin, login_url='no_autorizado')
def gestionar_usuarios(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        nuevo_rol = request.POST.get('rol')

        try:
            usuario = User.objects.get(id=user_id)

            if nuevo_rol == 'admin':
                usuario.is_staff = True
                usuario.is_superuser = True
            else:  # cliente
                usuario.is_staff = False
                usuario.is_superuser = False

            usuario.save()
        except User.DoesNotExist:
            pass

        return redirect('gestionar_usuarios')

    usuarios = User.objects.all()
    context = {
        'usuarios': usuarios,
        'usuario': request.user
    }
    return render(request, 'ferreteria/gestionar_usuarios.html', context)

def no_autorizado(request):
    return render(request, 'ferreteria/no_autorizado.html')

@user_passes_test(es_admin, login_url='no_autorizado')
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto añadido correctamente.')
            return redirect('agregar_producto')
        else:
            messages.error(request, 'No se logró añadir el producto.')
    else:
        form = ProductoForm()

    context = {
        'form': form,
        'usuario': request.user
    }
    return render(request, 'ferreteria/agregar_producto.html', context)

@user_passes_test(es_admin, login_url='no_autorizado')
def listar_productos(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
        'usuario': request.user
    }
    return render(request, 'ferreteria/listar_productos.html', context)

@user_passes_test(es_admin, login_url='no_autorizado')
def dashboard(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'ferreteria/dashboard_base.html', context)

def logout_usuario(request):
    logout(request)
    return redirect('login')