from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
    path('inicio/', views.vista_inicio, name='inicio'),
    path('logout/', LogoutView.as_view(next_page='registro'), name='logout'),
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/', views.listar_productos, name='listar_productos'),   
]
