from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/lista/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuarios, name='crear_usuarios'),
    path('usuarios/editar/<int:id>/', views.editar_usuarios, name='editar_usuarios'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuarios, name='eliminar_usuarios'),
    ]