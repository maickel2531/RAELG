from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/lista/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuarios, name='crear_usuarios'),
    path('usuarios/editar/<int:id>/', views.editar_usuarios, name='editar_usuarios'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuarios, name='eliminar_usuarios'),
    path('clientes/lista/', views.lista_cliente, name='lista_cliente'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('pedidos/lista/', views.lista_pedido, name='lista_pedido'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('recibos/lista/', views.lista_recibo_de_caja, name='lista_recibo_de_caja'),
    path('recibos/crear/', views.crear_recibo_de_caja, name='crear_recibo_de_caja'),
    path('recibos/editar/<int:id>/', views.editar_recibo_de_caja, name='editar_recibo_de_caja'),
    path('recibos/eliminar/<int:id>/', views.eliminar_recibo_de_caja, name='eliminar_recibo_de_caja'),
    path('garantias/lista/', views.lista_garantia, name='lista_garantia'),
    path('garantias/crear/', views.crear_garantia, name='crear_garantia'),
    path('garantias/editar/<int:id>/', views.editar_garantia, name='editar_garantia'),
    path('garantias/eliminar/<int:id>/', views.eliminar_garantia, name='eliminar_garantia'),
    ]