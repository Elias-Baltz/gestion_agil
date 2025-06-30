from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_usuario, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
    path('inicio/', views.vista_inicio, name='inicio'),
    
]
