import re
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Rol, Perfil, Usuario, Cliente, Producto, Pedido, Pago, Garantia, Remision, DetalleRemision
from .decoradores import rol_requerido


# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'index.html')
def inicio(request):
    return render(request, 'inicio.html')
    
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Verificar si el usuario existe
        if not User.objects.filter(username=username).exists():
            return render(request, 'login.html', {
                'error_username': 'El usuario no existe',
                'username': username  # Para que no se borre lo que escribió
            })

        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error_password': 'La contraseña es incorrecta',
                'username': username
            })

    return render(request, 'login.html')


# Función para validar contraseña
def validar_contraseña(password):
    patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
    return re.match(patron, password) 



def register_view(request):
    roles = Rol.objects.all()  # cargar roles

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        rol_id = request.POST.get('rol')

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'El usuario ya existe',
                'roles': roles
            })

        # Validar contraseña
        if not validar_contraseña(password):
            return render(request, 'register.html', {
                'error': 'La contraseña debe tener al menos una minúscula, una mayúscula, un número, un carácter especial y mínimo 8 caracteres.',
                'roles': roles
            })

        # Crear usuario
        user = User.objects.create_user(username=username, password=password, email=email)

        # Crear perfil con rol
        rol = Rol.objects.get(id=rol_id)
        Perfil.objects.create(user=user, rol=rol)

        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html', {'roles': roles})



def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
@rol_requerido('admin')
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'usuario/lista_usuarios.html', {'page_obj': page_obj})

@login_required
@rol_requerido('admin')
def crear_usuario(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        primer_nombre = request.POST.get('primer_nombre_usuario')
        segundo_nombre = request.POST.get('segundo_nombre_usuario', '')
        primer_apellido = request.POST.get('primer_apellido_usuario')
        segundo_apellido = request.POST.get('segundo_apellido_usuario', '')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña') # En un sistema real, no se debería guardar en texto plano
        rol_id = request.POST.get('rol')

        rol = Rol.objects.get(id=rol_id) if rol_id else None

        # Validar si el correo ya existe
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'usuario/crear_usuarios.html', {'roles': Rol.objects.all()})
            
        # Validaciones simples
        if not correo or not contraseña:
            messages.error(request, 'Correo y contraseña son obligatorios.')
        else:
    

            # Crear el usuario personalizado
            Usuario.objects.create(
                primer_nombre_usuario=primer_nombre,
                segundo_nombre_usuario=segundo_nombre,
                primer_apellido_usuario=primer_apellido,
                segundo_apellido_usuario=segundo_apellido,
                telefono=telefono,
                correo=correo,
                contraseña=contraseña, # ¡OJO! En un sistema real, usar hash
                Rol=rol
            )
            messages.success(request, f'Usuario "{primer_nombre}" creado exitosamente.')
            return redirect('lista_usuarios')

    roles = Rol.objects.all()
    return render(request, 'usuario/crear_usuarios.html', {'roles': roles})

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        # Obtener datos del formulario
        usuario.primer_nombre_usuario = request.POST.get('primer_nombre_usuario')
        usuario.segundo_nombre_usuario = request.POST.get('segundo_nombre_usuario', '')
        usuario.primer_apellido_usuario = request.POST.get('primer_apellido_usuario')
        usuario.segundo_apellido_usuario = request.POST.get('segundo_apellido_usuario', '')
        usuario.telefono = request.POST.get('telefono')
        usuario.correo = request.POST.get('correo')
        # No se actualiza la contraseña aquí por simplicidad
        rol_id = request.POST.get('Rol')
        usuario.Rol = Rol.objects.get(id=rol_id) if rol_id else None

        usuario.save()
        messages.success(request, f'Usuario "{usuario.primer_nombre_usuario}" actualizado exitosamente.')
        return redirect('lista_usuarios')

    roles = Rol.objects.all()
    return render(request, 'usuario/editar_usuarios.html', {'usuario': usuario, 'roles': roles})

@login_required
# views.py (modificar la vista eliminar_usuario)

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        nombre_usuario = f"{usuario.primer_nombre_usuario or ''} {usuario.primer_apellido_usuario or ''}".strip()
        try:
            usuario.delete()
            messages.success(request, f'Usuario "{nombre_usuario}" eliminado exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el usuario: {str(e)}')

    # Redirige de vuelta a la lista de usuarios después de intentar eliminar
    return redirect('lista_usuarios')

    # NOTA: El 'else' no es necesario si solo se maneja POST,
    # ya que cualquier acceso GET directo a esta URL redirigirá a la lista.
    # Si quieres que responda distinto a GET, puedes agregarlo:
    # else:
    #     messages.error(request, 'Método no permitido.')
    #     return redirect('lista_usuarios')


# --- VISTAS PARA CLIENTE ---

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cliente/lista_clientes.html', {'page_obj': page_obj})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        primer_nombre = request.POST.get('primer_nombre_cliente')
        segundo_nombre = request.POST.get('segundo_nombre_cliente', '')
        primer_apellido = request.POST.get('primer_apellido_cliente')
        segundo_apellido = request.POST.get('segundo_apellido_cliente', '')
        documento_id = request.POST.get('documento_id')
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono')
        correo_electronico = request.POST.get('correo_electronico', '')

        Cliente.objects.create(
            primer_nombre_cliente=primer_nombre,
            segundo_nombre_cliente=segundo_nombre,
            primer_apellido_cliente=primer_apellido,
            segundo_apellido_cliente=segundo_apellido,
            documento_id=documento_id,
            direccion=direccion,
            telefono=telefono,
            correo_electronico=correo_electronico
        )
        messages.success(request, f'Cliente "{primer_nombre} {primer_apellido}" creado exitosamente.')
        return redirect('lista_clientes')

    return render(request, 'cliente/crear_clientes.html')

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.primer_nombre_cliente = request.POST.get('primer_nombre_cliente')
        cliente.segundo_nombre_cliente = request.POST.get('segundo_nombre_cliente', '')
        cliente.primer_apellido_cliente = request.POST.get('primer_apellido_cliente')
        cliente.segundo_apellido_cliente = request.POST.get('segundo_apellido_cliente', '')
        cliente.documento_id = request.POST.get('documento_id')
        cliente.direccion = request.POST.get('direccion', '')
        cliente.telefono = request.POST.get('telefono')
        cliente.correo_electronico = request.POST.get('correo_electronico', '')

        cliente.save()
        messages.success(request, f'Cliente "{cliente.primer_nombre_cliente} {cliente.primer_apellido_cliente}" actualizado exitosamente.')
        return redirect('lista_clientes')

    return render(request, 'cliente/editar_clientes.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        nombre_cliente = f"{cliente.primer_nombre_cliente or ''} {cliente.primer_apellido_cliente or ''}".strip()
        try:
            cliente.delete()
            messages.success(request, f'Cliente "{nombre_cliente}" eliminado exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el cliente: {str(e)}')

    # Redirige de vuelta a la lista de clientes después de intentar eliminar
    return redirect('lista_clientes')

# --- VISTAS PARA PRODUCTO ---

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'producto/lista_productos.html', {'page_obj': page_obj})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        descripcion_producto = request.POST.get('descripcion_producto', '')
        precio_venta = request.POST.get('precio_venta')
        costo_unitario = request.POST.get('costo_unitario')

        try:
            Producto.objects.create(
                nombre_producto=nombre_producto,
                descripcion_producto=descripcion_producto,
                precio_venta=precio_venta,
                costo_unitario=costo_unitario
            )
            messages.success(request, f'Producto "{nombre_producto}" creado exitosamente.')
            return redirect('lista_productos')
        except ValueError:
            messages.error(request, 'Error al crear el producto. Asegúrese de ingresar valores numéricos válidos para precio y costo.')

    return render(request, 'producto/crear_productos.html')

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.descripcion_producto = request.POST.get('descripcion_producto', '')
        precio_venta_str = request.POST.get('precio_venta')
        costo_unitario_str = request.POST.get('costo_unitario')

        try:
            producto.precio_venta = precio_venta_str
            producto.costo_unitario = costo_unitario_str
            producto.save()
            messages.success(request, f'Producto "{producto.nombre_producto}" actualizado exitosamente.')
            return redirect('lista_productos')
        except ValueError:
            messages.error(request, 'Error al actualizar el producto. Asegúrese de ingresar valores numéricos válidos para precio y costo.')

    return render(request, 'producto/editar_productos.html', {'producto': producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST': 
        nombre_producto = f"{producto.nombre_producto or ''}".strip()
        try:
            producto.delete()
            messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el producto: {str(e)}')

    return redirect('lista_productos')

# --- VISTAS PARA PEDIDO ---

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente', 'producto', 'responsable').all()
    paginator = Paginator(pedidos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pedido/lista_pedidos.html', {'page_obj': page_obj})

# views.py

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        pedido_numero = request.POST.get('pedido')
        producto_id = request.POST.get('producto')
        cliente_id = request.POST.get('cliente')
        fecha_pedido = request.POST.get('fecha_pedido')
        fecha_entrega = request.POST.get('fecha_entrega')
        cantidad_str = request.POST.get('cantidad')
        responsable_id = request.POST.get('responsable')

        try:
            producto = Producto.objects.get(id=producto_id) if producto_id else None
            cliente = Cliente.objects.get(id=cliente_id)
            responsable = Usuario.objects.get(id=responsable_id) if responsable_id else None

            cantidad = int(cantidad_str) if cantidad_str else 0

            Pedido.objects.create(
                pedido=pedido_numero,
                producto=producto,
                cliente=cliente,
                fecha_pedido=fecha_pedido,
                fecha_entrega=fecha_entrega,
                cantidad=cantidad,
                # No se asigna valor_total aquí, ya que no existe en el modelo
                responsable=responsable
            )
            messages.success(request, f'Pedido "{pedido_numero}" creado exitosamente.')
            return redirect('lista_pedidos')
        except (Producto.DoesNotExist, Cliente.DoesNotExist, Usuario.DoesNotExist):
            messages.error(request, 'Producto, Cliente o Responsable no encontrado.')
        except ValueError:
            messages.error(request, 'La cantidad debe ser un número entero válido.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'pedido/crear_pedidos.html', {
        'clientes': clientes,
        'productos': productos,
        'usuarios': usuarios
    })

@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.pedido = request.POST.get('pedido')
        producto_id = request.POST.get('producto')
        cliente_id = request.POST.get('cliente')
        responsable_id = request.POST.get('responsable')
        cantidad_str = request.POST.get('cantidad')

        pedido.producto = Producto.objects.get(id=producto_id) if producto_id else None
        pedido.cliente = Cliente.objects.get(id=cliente_id)
        pedido.fecha_pedido = request.POST.get('fecha_pedido')
        pedido.fecha_entrega = request.POST.get('fecha_entrega')
        pedido.cantidad = int(cantidad_str) if cantidad_str else 0
        pedido.responsable = Usuario.objects.get(id=responsable_id) if responsable_id else None

        try:
            pedido.save()
            messages.success(request, f'Pedido "{pedido.pedido}" actualizado exitosamente.')
            return redirect('lista_pedidos')
        except (Producto.DoesNotExist, Cliente.DoesNotExist, Usuario.DoesNotExist):
            messages.error(request, 'Producto, Cliente o Responsable no encontrado.')
        except ValueError:
            messages.error(request, 'La cantidad debe ser un número entero válido.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'pedido/editar_pedidos.html', {
        'pedido': pedido,
        'clientes': clientes,
        'productos': productos,
        'usuarios': usuarios
    })


@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido_numero = pedido.pedido
        try:
            pedido.delete()
            messages.success(request, f'Pedido "{pedido_numero}" eliminado exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el pedido: {str(e)}')

    return redirect('lista_pedidos')

# --- VISTAS PARA PAGO ---

@login_required
def lista_pagos(request):
    pagos = Pago.objects.select_related('pedido', 'cliente').all()
    paginator = Paginator(pagos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pago/lista_pagos.html', {'page_obj': page_obj})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido')
        cliente_id = request.POST.get('cliente')
        fecha_pago = request.POST.get('fecha_pago')
        monto_pago = request.POST.get('monto_pago')
        observaciones = request.POST.get('observaciones', '')

        try:
            pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None
            cliente = Cliente.objects.get(id=cliente_id)

            Pago.objects.create(
                pedido=pedido,
                cliente=cliente,
                fecha_pago=fecha_pago,
                monto_pago=monto_pago,
                observaciones=observaciones
            )
            messages.success(request, f'Pago de ${monto_pago} registrado exitosamente.')
            return redirect('lista_pagos')
        except (Pedido.DoesNotExist, Cliente.DoesNotExist):
            messages.error(request, 'Pedido o Cliente no encontrado.')

    pedidos = Pedido.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pago/crear_pagos.html', {
        'pedidos': pedidos,
        'clientes': clientes
    })

@login_required
def editar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido')
        cliente_id = request.POST.get('cliente')
        pago.fecha_pago = request.POST.get('fecha_pago')
        pago.monto_pago = request.POST.get('monto_pago')
        pago.observaciones = request.POST.get('observaciones', '')

        try:
            pago.pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None
            pago.cliente = Cliente.objects.get(id=cliente_id)
            pago.save()
            messages.success(request, f'Pago de ${pago.monto_pago} actualizado exitosamente.')
            return redirect('lista_pagos')
        except (Pedido.DoesNotExist, Cliente.DoesNotExist):
            messages.error(request, 'Pedido o Cliente no encontrado.')

    pedidos = Pedido.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'pago/editar_pagos.html', {
        'pago': pago,
        'pedidos': pedidos,
        'clientes': clientes
    })

@login_required
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id) if pago_id else None
    if request.method == 'POST':
        pago_numero = pago.id
        try: 
            pago.delete()
            messages.success(request, f'Pago de ${pago_numero} eliminado exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el pago: {str(e)}')
    return redirect('lista_pagos')
# --- VISTAS PARA GARANTIA ---

@login_required
def lista_garantias(request):
    garantias = Garantia.objects.select_related('cliente', 'producto', 'pedido').all()
    paginator = Paginator(garantias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'garantia/lista_garantias.html', {'page_obj': page_obj})

@login_required
def crear_garantia(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        producto_id = request.POST.get('producto')
        pedido_id = request.POST.get('pedido')
        motivo_reclamo = request.POST.get('motivo_reclamo')
        fecha_reclamo = request.POST.get('fecha_reclamo')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            producto = Producto.objects.get(id=producto_id) if producto_id else None
            pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None

            Garantia.objects.create(
                cliente=cliente,
                producto=producto,
                pedido=pedido,
                motivo_reclamo=motivo_reclamo,
                fecha_reclamo=fecha_reclamo
            )
            messages.success(request, f'Garantía registrada exitosamente para el cliente y producto.')
            return redirect('lista_garantias')
        except (Cliente.DoesNotExist, Producto.DoesNotExist, Pedido.DoesNotExist):
            messages.error(request, 'Cliente, Producto o Pedido no encontrado.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'garantia/crear_garantias.html', {
        'clientes': clientes,
        'productos': productos,
        'pedidos': pedidos
    })

@login_required
def editar_garantia(request, garantia_id):
    garantia = get_object_or_404(Garantia, id=garantia_id)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        producto_id = request.POST.get('producto')
        pedido_id = request.POST.get('pedido')
        garantia.motivo_reclamo = request.POST.get('motivo_reclamo')
        garantia.fecha_reclamo = request.POST.get('fecha_reclamo')

        try:
            garantia.cliente = Cliente.objects.get(id=cliente_id)
            garantia.producto = Producto.objects.get(id=producto_id) if producto_id else None
            garantia.pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None
            garantia.save()
            messages.success(request, f'Garantía actualizada exitosamente.')
            return redirect('lista_garantias')
        except (Cliente.DoesNotExist, Producto.DoesNotExist, Pedido.DoesNotExist):
            messages.error(request, 'Cliente, Producto o Pedido no encontrado.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    pedidos = Pedido.objects.all()
    return render(request, 'garantia/editar_garantias.html', {
        'garantia': garantia,
        'clientes': clientes,
        'productos': productos,
        'pedidos': pedidos
    })

@login_required
def eliminar_garantia(request, garantia_id):
    garantia = get_object_or_404(Garantia, id=garantia_id) if garantia_id else None
    if request.method == 'POST':
        garantia_numero = garantia.id
        try:
            garantia.delete()
            messages.success(request, f'Garantía eliminada exitosamente.')
        except Exception as e:
            # Opcional: Manejar errores específicos si es necesario
            messages.error(request, f'Error al eliminar el garantía: {str(e)}')
    return redirect('lista_garantias')
# --- FIN DE VISTAS PARA GARANTIA ---
# --- VISTAS PARA REMISIONES ---
@login_required
def remision_pdf(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    
    # Calcular total general
    total_general = sum(item.valor_total for item in remision.detalles.all())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="remision_{remision.id}.pdf"'  # usa 'attachment' si quieres forzar descarga

    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#2c3e50")
    )
    normal = styles["Normal"]
    right_align = ParagraphStyle('Right', parent=normal, alignment=TA_RIGHT)

    # Encabezado
    elements.append(Paragraph("CASA MOBLER", title_style))
    elements.append(Paragraph("REMISIÓN DE ENTREGA", styles['Heading2']))
    elements.append(Paragraph(f"Número: {remision.id} &nbsp; | &nbsp; Fecha: {remision.fecha_emision}", normal))
    elements.append(Spacer(1, 20))

    # Datos del cliente
    cliente = remision.cliente
    nombre_completo = " ".join(filter(None, [
        cliente.primer_nombre_cliente,
        cliente.segundo_nombre_cliente,
        cliente.primer_apellido_cliente,
        cliente.segundo_apellido_cliente
    ]))
    elements.append(Paragraph("<b>Datos del Cliente</b>", styles['Heading3']))
    elements.append(Paragraph(f"Nombre: {nombre_completo}", normal))
    elements.append(Paragraph(f"Documento ID: {cliente.documento_id}", normal))
    elements.append(Paragraph(f"Teléfono: {cliente.telefono}", normal))
    elements.append(Paragraph(f"Dirección: {cliente.direccion}", normal))
    if remision.fecha_entrega_estimada:
        elements.append(Paragraph(f"Fecha de entrega estimada: {remision.fecha_entrega_estimada}", normal))
    elements.append(Spacer(1, 15))

    # Tabla de productos
    data = [["Producto", "Cantidad", "Valor Unitario", "Valor Total"]]
    for item in remision.detalles.all():
        data.append([
            item.producto.nombre_producto,
            str(item.cantidad),
            f"${item.valor_unitario:,.0f}",
            f"${item.valor_total:,.0f}"
        ])

    table = Table(data, colWidths=[200, 60, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # Total
    elements.append(Paragraph(f"<b>Total a entregar: ${total_general:,.0f}</b>", right_align))
    elements.append(Spacer(1, 15))

    # Observaciones
    if remision.observaciones:
        elements.append(Paragraph("<b>Observaciones:</b>", styles['Heading4']))
        elements.append(Paragraph(remision.observaciones.replace('\n', '<br/>'), normal))

    doc.build(elements)
    return response

@login_required
@login_required
def detalle_remision(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    total_general = sum(item.valor_total for item in remision.detalles.all())
    return render(request, 'remisiones/detalle_remision.html', {
        'remision': remision,
        'total_general': total_general
    })

@login_required
def lista_remisiones(request):
    remisiones = Remision.objects.select_related('cliente').prefetch_related('detalles__producto').all()
    paginator = Paginator(remisiones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'remisiones/lista_remisiones.html', {'page_obj': page_obj})

@login_required
def crear_remision(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        fecha_entrega = request.POST.get('fecha_entrega_estimada')
        observaciones = request.POST.get('observaciones', '')
        producto_ids = request.POST.getlist('producto_id')
        cantidades = request.POST.getlist('cantidad')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            # Crear la remisión
            remision = Remision.objects.create(
                cliente=cliente,
                fecha_entrega_estimada=fecha_entrega,
                observaciones=observaciones
            )

            # Crear los detalles
            for prod_id, cant in zip(producto_ids, cantidades):
                if prod_id and cant and int(cant) > 0:
                    producto = Producto.objects.get(id=prod_id)
                    DetalleRemision.objects.create(
                        remision=remision,
                        producto=producto,
                        cantidad=int(cant)
                    )

            messages.success(request, f'Remisión #{remision.id} creada exitosamente.')
            return redirect('lista_remisiones')

        except Exception as e:
            messages.error(request, f'Error al crear la remisión: {str(e)}')

    # Cargar datos para el formulario
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'remisiones/crear_remision.html', {
        'clientes': clientes,
        'productos': productos
    })
