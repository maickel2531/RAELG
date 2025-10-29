import re
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from django.contrib.auth.hashers import make_password
from .models import Rol, Perfil, Cliente, Producto, Pedido, Pago, Garantia, Remision, DetalleRemision
from .forms import ProductoForm  
from django.shortcuts import render, redirect
from django.contrib import messages     


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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error_password': 'Credenciales inválidas'})
    return render(request, 'login.html')  # ← render(request, ...)

# Función para validar contraseña
def validar_contraseña(password):
    patron = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
    return re.match(patron, password) 

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
@rol_requerido('admin')
def lista_usuarios(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).select_related('perfil__rol')
    else:
        users = User.objects.select_related('perfil__rol').all()

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'usuario/lista_usuarios.html', {'page_obj': page_obj})

@login_required
@rol_requerido('admin')
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name', '')
        last_name = request.POST.get('last_name')
        second_last_name = request.POST.get('second_last_name', '')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        rol_id = request.POST.get('rol')

        # Validaciones
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuario/crear_usuarios.html', {'roles': Rol.objects.all()})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'usuario/crear_usuarios.html', {'roles': Rol.objects.all()})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return render(request, 'usuario/crear_usuarios.html', {'roles': Rol.objects.all()})

        # Crear usuario → esto dispara la señal y crea un Perfil vacío
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        perfil = Perfil.objects.create(
            user=user,
            second_name=second_name,
            second_last_name=second_last_name,
            telefono=telefono,
            rol_id=rol_id
        )
        # Actualizar los campos adicionales
        perfil.second_name = second_name
        perfil.second_last_name = second_last_name
        perfil.telefono = telefono
        perfil.rol_id = rol_id
        perfil.save()

        messages.success(request, f'Usuario "{username}" creado exitosamente.')
        return redirect('lista_usuarios')

    roles = Rol.objects.all()
    return render(request, 'usuario/crear_usuarios.html', {'roles': roles})

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    perfil, created = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        perfil.telefono = request.POST.get('telefono')
        perfil.rol_id = request.POST.get('rol')
        rol_id = request.POST.get('rol')
        if rol_id:
            perfil.rol_id = rol_id  # o: perfil.rol = Rol.objects.get(id=rol_id)
        else:
            perfil.rol = None
        user.save()
        perfil.save()
        messages.success(request, 'Usuario actualizado.')
        return redirect('lista_usuarios')  # ← Redirect a la lista de usuarios
    roles = Rol.objects.all()

    return render(request, 'usuario/editar_usuarios.html', {
        'user': user,
        'perfil': perfil,
        'roles': roles
    })
# views.py (modificar la vista eliminar_usuario)

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()  # ¡Esto elimina también el Perfil (por CASCADE)!
        messages.success(request, 'Usuario eliminado.')
        return redirect('lista_usuarios')
# --- VISTAS PARA CLIENTE ---

@login_required
def lista_clientes(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(
            Q(primer_nombre_cliente__icontains=query) |
            Q(segundo_nombre_cliente__icontains=query) |
            Q(primer_apellido_cliente__icontains=query) |
            Q(segundo_apellido_cliente__icontains=query) |
            Q(documento_id__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo_electronico__icontains=query)
        ).all()
    else:
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
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(
            Q(nombre_producto__icontains=query) |
            Q(descripcion_producto__icontains=query) |
            Q(precio_venta__icontains=query) |
            Q(costo_unitario__icontains=query)
        ).all()
    else:
        productos = Producto.objects.all()  
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'producto/lista_productos.html', {'page_obj': page_obj})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente ✅")
            return redirect('lista_productos')
        else:
            # Mostrar errores para identificar por qué no se renderizan o validan campos
            messages.error(request, f"Error formulario: {form.errors}")
    else:
        form = ProductoForm()

    return render(request, 'producto/crear_productos.html', {'form': form})

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
    query = request.GET.get('q')
    if query:
        pedidos = Pedido.objects.filter(
            Q(id__icontains=query) |
            Q(cliente__primer_nombre_cliente__icontains=query) |
            Q(cliente__primer_apellido_cliente__icontains=query) |
            Q(producto__nombre_producto__icontains=query)        # User
        ).select_related('cliente', 'producto')
    else:
        pedidos = Pedido.objects.select_related('cliente', 'producto')

    paginator = Paginator(pedidos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
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

        try:
            producto = Producto.objects.get(id=producto_id) if producto_id else None
            cliente = Cliente.objects.get(id=cliente_id)

            cantidad = int(cantidad_str) if cantidad_str else 0

            Pedido.objects.create(
                pedido=pedido_numero,
                producto=producto,
                cliente=cliente,
                fecha_pedido=fecha_pedido,
                fecha_entrega=fecha_entrega,
                cantidad=cantidad,
            )
            messages.success(request, f'Pedido "{pedido_numero}" creado exitosamente.')
            return redirect('lista_pedidos')
        except (Producto.DoesNotExist, Cliente.DoesNotExist):
            messages.error(request, 'Producto, Cliente no encontrado.')
        except ValueError:
            messages.error(request, 'La cantidad debe ser un número entero válido.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'pedido/crear_pedidos.html', {
        'clientes': clientes,
        'productos': productos
    })

@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.pedido = request.POST.get('pedido')
        producto_id = request.POST.get('producto')
        cliente_id = request.POST.get('cliente')
        cantidad_str = request.POST.get('cantidad')

        try:
            pedido.producto = Producto.objects.get(id=producto_id) if producto_id else None
            pedido.cliente = Cliente.objects.get(id=cliente_id)
            pedido.fecha_pedido = request.POST.get('fecha_pedido')
            pedido.fecha_entrega = request.POST.get('fecha_entrega')
            pedido.cantidad = int(cantidad_str) if cantidad_str else 0

            pedido.save()
            messages.success(request, f'Pedido "{pedido.pedido}" actualizado exitosamente.')
            return redirect('lista_pedidos')
        except (Producto.DoesNotExist, Cliente.DoesNotExist):
            messages.error(request, 'Producto, Cliente no encontrado.')
        except ValueError:
            messages.error(request, 'La cantidad debe ser un número entero válido.')

    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'pedido/editar_pedidos.html', {
        'pedido': pedido,
        'clientes': clientes,
        'productos': productos,
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
    query = request.GET.get('q')
    if query:
        pagos = Pago.objects.filter(
            Q(id__icontains=query) |
            Q(cliente__primer_nombre_cliente__icontains=query) |
            Q(cliente__primer_apellido_cliente__icontains=query) |
            Q(cliente__documento_id__icontains=query) |
            Q(pedido__pedido__icontains=query)
        ).select_related('pedido', 'cliente').all()
    else:
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
    query = request.GET.get('q')
    if query:
        garantias = Garantia.objects.filter(
            Q(cliente__primer_nombre_cliente__icontains=query) |
            Q(cliente__primer_apellido_cliente__icontains=query) |
            Q(cliente__documento_id__icontains=query) |
            Q(producto__nombre_producto__icontains=query) |
            Q(pedido__pedido__icontains=query)
        ).select_related('cliente', 'producto', 'pedido').all()
    else:
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
    total_general = sum(item.valor_total for item in remision.detalles.all())

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="remision_{remision.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=40, bottomMargin=40, leftMargin=40, rightMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # === COLORES ===
    COLOR_RED = colors.HexColor("#e31b23")  # Rojo vibrante (ajusta según tu marca)
    COLOR_BLACK = colors.HexColor("#000000")
    COLOR_DARK_GRAY = colors.HexColor("#333333")
    COLOR_LIGHT_GRAY = colors.HexColor("#f5f5f5")

    # === ESTILOS PERSONALIZADOS ===
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=8,
        textColor=COLOR_BLACK,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=COLOR_RED,
        fontName='Helvetica-Bold'
    )

    header_style = ParagraphStyle(
        'Header',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=COLOR_BLACK,
        fontName='Helvetica'
    )

    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=COLOR_BLACK,
        fontName='Helvetica-Bold',
        spaceAfter=8,
        spaceBefore=12
    )

    normal_style = ParagraphStyle(
        'Normal',
        fontSize=10,
        textColor=COLOR_DARK_GRAY,
        fontName='Helvetica'
    )

    total_style = ParagraphStyle(
        'Total',
        fontSize=12,
        alignment=TA_RIGHT,
        textColor=COLOR_RED,
        fontName='Helvetica-Bold'
    )

    # === ENCABEZADO ===
    elements.append(Paragraph("CASA MOBLER", title_style))
    elements.append(Paragraph("REMISIÓN DE ENTREGA", subtitle_style))
    elements.append(Paragraph(f"Número: <b>{remision.id}</b> &nbsp; | &nbsp; Fecha: <b>{remision.fecha_emision}</b>", header_style))
    elements.append(Spacer(1, 20))

    # === DATOS DEL CLIENTE ===
    cliente = remision.cliente
    nombre_completo = " ".join(filter(None, [
        cliente.primer_nombre_cliente,
        cliente.segundo_nombre_cliente,
        cliente.primer_apellido_cliente,
        cliente.segundo_apellido_cliente
    ]))

    elements.append(Paragraph("DATOS DEL CLIENTE", section_title))
    elements.append(Paragraph(f"<b>Nombre:</b> {nombre_completo}", normal_style))
    elements.append(Paragraph(f"<b>Documento ID:</b> {cliente.documento_id}", normal_style))
    elements.append(Paragraph(f"<b>Teléfono:</b> {cliente.telefono}", normal_style))
    elements.append(Paragraph(f"<b>Dirección:</b> {cliente.direccion}", normal_style))
    if remision.fecha_entrega_estimada:
        elements.append(Paragraph(f"<b>Fecha de entrega estimada:</b> {remision.fecha_entrega_estimada}", normal_style))
    elements.append(Spacer(1, 15))

    # === TABLA DE PRODUCTOS ===
    data = [
        ["PRODUCTO", "CANTIDAD", "VALOR UNITARIO", "VALOR TOTAL"]
    ]
    for item in remision.detalles.all():
        data.append([
            item.producto.nombre_producto,
            str(item.cantidad),
            f"${item.valor_unitario:,.0f}",
            f"${item.valor_total:,.0f}"
        ])

    # Anchos de columna ajustados
    col_widths = [220, 70, 90, 90]

    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        # Cabecera
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_RED),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, 0), 8),

        # Cuerpo
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BLACK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_GRAY]),
        ('PADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # === TOTAL ===
    elements.append(Paragraph(f"TOTAL A ENTREGAR: <b>${total_general:,.0f}</b>", total_style))
    elements.append(Spacer(1, 15))

    # === OBSERVACIONES ===
    if remision.observaciones:
        elements.append(Paragraph("OBSERVACIONES", section_title))
        obs_text = remision.observaciones.replace('\n', '<br/>')
        elements.append(Paragraph(obs_text, normal_style))

    # === PIE DE PÁGINA (opcional) ===
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<i>Documento válido sin firma. Generado electrónicamente.</i>", ParagraphStyle(
        'Footer',
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey,
        fontName='Helvetica-Oblique'
    )))

    doc.build(elements)
    return response

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
    query = request.GET.get('q')
    if query:
        remisiones = Remision.objects.filter(
            Q(id__icontains=query) |
            Q(cliente__primer_nombre_cliente__icontains=query) |
            Q(cliente__primer_apellido_cliente__icontains=query) |
            Q(cliente__documento_id__icontains=query)
        ).select_related('cliente').prefetch_related('detalles__producto').all()
    else:
        remisiones = Remision.objects.select_related('cliente').prefetch_related('detalles__producto').all()

    paginator = Paginator(remisiones, 10)  # 10 remisiones por página
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
    return render(request, 'remisiones/lista_remisiones.html', {'page_obj': page_obj})

@login_required
def eliminar_remision(request, remision_id):
    remision = get_object_or_404(Remision, id=remision_id)
    if request.method == 'POST':
        remision_id_guardado = remision.id
        remision.delete()
        messages.success(request, f'Remisión #{remision_id_guardado} eliminada exitosamente.')
        return redirect('lista_remisiones')
    
    # Si es GET, redirige (opcional: podrías mostrar una página de confirmación)
    return redirect('lista_remisiones')