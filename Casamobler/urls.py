from django.contrib import admin
from django.urls import path , include
from Casamobler import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard
    path('login/', views.login_view, name='login'),         # Login
    path('logout/', views.logout_view, name='logout'),      # Logout
    path('register/', views.register_view, name='register'),      # Registro    
    path('inicio/', views.inicio, name='inicio'),      # Inicio
    path('', views.index, name='index'),
        # USUARIO (Modelo Personalizado)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuarios'),
    path('usuarios/<int:usuario_id>/editar/', views.editar_usuario, name='editar_usuarios'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuarios'),

    # CLIENTE
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_clientes'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_clientes'),
    path('clientes/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_clientes'),

    # PRODUCTO
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_productos'),
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_productos'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_productos'),

    # PEDIDO
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedidos'),
    path('pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedidos'),
    path('pedidos/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedidos'),

    # PAGO
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/crear/', views.crear_pago, name='crear_pagos'),
    path('pagos/<int:pago_id>/editar/', views.editar_pago, name='editar_pagos'),
    path('pagos/<int:pago_id>/eliminar/', views.eliminar_pago, name='eliminar_pagos'),

    # GARANTIA
    path('garantias/', views.lista_garantias, name='lista_garantias'),
    path('garantias/crear/', views.crear_garantia, name='crear_garantias'),
    path('garantias/<int:garantia_id>/editar/', views.editar_garantia, name='editar_garantias'),
    path('garantias/<int:garantia_id>/eliminar/', views.eliminar_garantia, name='eliminar_garantias'),
  
    ]
    # myapp/urls.py (añadir después de tus URLs existentes)

