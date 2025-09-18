import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol, Cliente, Pedido ,ReciboCaja , Garantia , Perfil

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


from .models import Rol, Perfil

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

def lista_usuarios(request):
    return render(request, 'usuario/lista_usuarios.html', {'usuarios': Usuario.objects.all()})

def crear_usuarios(request):
    roles = Rol.objects.all()  # cargar roles
    if request.method == 'POST':  # Verificar si el usuario ya existe
        p_nombre = request.POST.get('p_nombre')
        s_nombre = request.POST.get('s_nombre')
        p_apellido = request.POST.get('p_apellido')
        s_apellido = request.POST.get('s_apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        rol = Rol.objects.get(id=request.POST.get('rol'))
        contraseña = request.POST.get('contraseña')
         # Crear usuario    
        Usuario.objects.create(p_nombre=p_nombre, s_nombre=s_nombre, p_apellido=p_apellido, s_apellido=s_apellido, correo=correo, telefono=telefono, contraseña=contraseña, rol=rol)
        return redirect('lista_usuarios')  # Redireccionar al usuario creado
    return render(request, 'usuario/crear_usuarios.html', {'roles': roles})  # Mostrar el formulario de creación de usuario


def eliminar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('lista_usuarios')

def editar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    roles = Rol.objects.all()
    if request.method == 'POST':
        rol = Rol.objects.get(id=request.POST.get('rol'))
        usuario.p_nombre = request.POST.get('p_nombre')
        usuario.s_nombre = request.POST.get('s_nombre')
        usuario.p_apellido = request.POST.get('p_apellido')
        usuario.s_apellido = request.POST.get('s_apellido')
        usuario.correo = request.POST.get('email')
        usuario.telefono = request.POST.get('telefono')
        usuario.contraseña = request.POST.get('contraseña')  # ⚠ Hashear en producción
        usuario.rol = rol
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'usuario/editar_usuarios.html', {'usuario': usuario, 'roles': roles})


def crear_cliente(request):
    if request.method == 'POST':
        primer_nombre = request.POST.get('p_nombrec')
        segundo_nombre = request.POST.get('s_nombrec')
        primer_apellido = request.POST.get('p_apellidoc')
        segundo_apellido = request.POST.get('s_apellido')
        documento_id = request.POST.get('documento_id')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono') if request.POST.get('telefono') else None
        correo_electronico = request.POST.get('correo_electronico')
        Cliente.objects.create(
            p_nombrec=primer_nombre,
            s_nombrec=segundo_nombre,
            p_apellidoc=primer_apellido,
            s_apellidoc=segundo_apellido,
            documento_id=documento_id,
            direccion=direccion,
            telefono=telefono,
            correo_electronico=correo_electronico
        )
        return redirect('lista_cliente')
    return render(request, 'cliente/crear_cliente.html')

def lista_cliente(request):
    return render(request, 'cliente/lista_cliente.html', {'clientes': Cliente.objects.all()})


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        primer_nombre = request.POST.get('p_nombrec')
        segundo_nombre = request.POST.get('s_nombrec')
        primer_apellido = request.POST.get('p_apellidoc')
        segundo_apellido = request.POST.get('s_apellidoc')
        documento_id = request.POST.get('documento_id') if request.POST.get('documento_id') else None
        direccion = request.POST.get('direccion') if request.POST.get('direccion') else None
        telefono = request.POST.get('telefono') if request.POST.get('telefono') else None
        correo_electronico = request.POST.get('correo_electronico') if request.POST.get('correo_electronico') else None
        cliente.p_nombrec = primer_nombre
        cliente.s_nombrec = segundo_nombre
        cliente.p_apellidoc = primer_apellido
        cliente.s_apellidoc = segundo_apellido
        cliente.documento_id = documento_id
        cliente.direccion = direccion
        cliente.telefono = telefono
        cliente.correo_electronico = correo_electronico
        cliente.save()
        return redirect('lista_cliente')
    return render(request, 'cliente/editar_cliente.html', {'cliente': cliente}) 

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_cliente')

def lista_pedido(request):
    return render(request, 'pedido/lista_pedido.html', {'pedidos': Pedido.objects.all()})

def crear_pedido(request):
    if request.method == 'POST':
        fecha_pedido = request.POST.get('fecha_pedido')
        fecha_entrega = request.POST.get('fecha_entrega')
        descripcion_producto = request.POST.get('descripcion_producto')
        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')
        cliente = Cliente.objects.get(id=request.POST.get('p_nombrec'))
        responsable_id = request.POST.get('responsable')
        responsable = Usuario.objects.get(id=responsable_id)
        Pedido.objects.create(
            fecha_pedido=fecha_pedido,
            fecha_entrega=fecha_entrega,
            descripcion_producto=descripcion_producto,
            cantidad=cantidad,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            cliente=cliente,
            responsable=responsable
        )
        return redirect('lista_pedido')
    return render(request, 'pedido/crear_pedido.html', {'clientes': Cliente.objects.all(), 'usuarios': Usuario.objects.all()})

        
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        cliente = Cliente.objects.get(id=request.POST.get('p_nombrec'))
        responsable = Usuario.objects.get(id=request.POST.get('p_nombre'))
        pedido.fecha_pedido = request.POST.get('fecha_pedido')
        pedido.fecha_entrega = request.POST.get('fecha_entrega')
        pedido.descripcion_producto = request.POST.get('descripcion_producto')
        pedido.cantidad = request.POST.get('cantidad')
        pedido.valor_unitario = request.POST.get('valor_unitario')
        pedido.valor_total = request.POST.get('valor_total')
        pedido.cliente = cliente
        pedido.responsable = responsable
        pedido.save()
        return redirect('lista_pedido')
    return render(request, 'pedido/editar_pedido.html', {'pedido': pedido, 'clientes': Cliente.objects.all(), 'usuarios': Usuario.objects.all()})


def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    return redirect('lista_pedido')

def lista_recibo_de_caja(request):
    return render(request, 'recibo/lista_recibo_de_caja.html', {'recibos': ReciboCaja.objects.all()})

def crear_recibo_de_caja(request):
    clientes = Cliente.objects.all()
    if request.method == "POST":
        pedido = Pedido.objects.get(id=request.POST.get("descripcion_producto"))
        fecha_recibo = request.POST.get("fecha_recibo")
        valor_abonado = request.POST.get("valor_abonado")
        forma_pago = request.POST.get("forma_pago")
        cliente = Cliente.objects.get(id=request.POST.get("p_nombrec"))
        direccion = request.POST.get("direccion")
        concepto = request.POST.get("concepto")
        ReciboCaja.objects.create(
            pedido=pedido,
            fecha_recibo=fecha_recibo,
            valor_abonado=valor_abonado,
            forma_pago=forma_pago,
            cliente=cliente,
            direccion=direccion,
            concepto=concepto
        )
        return redirect("lista_recibo_de_caja")
    return render(request, "recibo/crear_recibo_de_caja.html", {
        "pedidos": Pedido.objects.all(),
        'clientes': clientes
    })

def editar_recibo_de_caja(request, id):
    recibo = ReciboCaja.objects.get(id=id)
    if request.method == "POST":
        recibo.pedido = Pedido.objects.get(id=request.POST.get("descripcion_producto"))
        recibo.fecha_recibo = request.POST.get("fecha_recibo")
        recibo.valor_abonado = request.POST.get("valor_abonado")
        recibo.forma_pago = request.POST.get("forma_pago")
        recibo.cliente = Cliente.objects.get(id=request.POST.get("p_nombrec"))
        recibo.direccion = request.POST.get("direccion")
        recibo.concepto = request.POST.get("concepto")
        recibo.save()
        return redirect("lista_recibo_de_caja")
    return render(request, "recibo/editar_recibo_de_caja.html", {
        "recibo": recibo,
        "pedidos": Pedido.objects.all()
    })

def eliminar_recibo_de_caja(request, id):
    recibo = get_object_or_404(ReciboCaja, id=id)
    recibo.delete()
    return redirect('lista_recibo_de_caja')

def lista_garantia(request):
    return render(request, 'garantia/lista_garantia.html', {'garantias': Garantia.objects.all()})


def crear_garantia(request):
    clientes = Cliente.objects.all()
    pedidos = Pedido.objects.all()
    if request.method == 'POST':
        producto = request.POST.get('producto')
        motivo_reclamo = request.POST.get('motivo_reclamo')
        fecha_reclamo = request.POST.get('fecha_reclamo')
        estado_garantia = request.POST.get('estado_garantia')
        observaciones = request.POST.get('observaciones')
        cliente_id = request.POST.get('p_nombrec')
        pedido_id = request.POST.get('descripcion_producto')
        cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None
        pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None
        Garantia.objects.create(
            producto=producto,
            motivo_reclamo=motivo_reclamo,
            fecha_reclamo=fecha_reclamo,
            estado_garantia=estado_garantia,
            observaciones=observaciones,
            cliente=cliente,
            pedido=pedido
        )
        return redirect('lista_garantia')
    return render(request, 'garantia/crear_garantia.html', {'clientes': clientes, 'pedidos': pedidos})




def editar_garantia(request, id):
    garantia = get_object_or_404(Garantia, id=id)
    if request.method == 'POST':
        producto = request.POST.get('producto')
        motivo_reclamo = request.POST.get('motivo_reclamo')
        fecha_reclamo = request.POST.get('fecha_reclamo')
        estado_garantia = request.POST.get('estado_garantia')
        observaciones = request.POST.get('observaciones')
        cliente_id = request.POST.get('p_nombrec')
        pedido_id = request.POST.get('descripcion_producto')
        cliente = Cliente.objects.get(id=cliente_id) if cliente_id else None
        pedido = Pedido.objects.get(id=pedido_id) if pedido_id else None
        garantia.producto = producto
        garantia.motivo_reclamo = motivo_reclamo
        garantia.fecha_reclamo = fecha_reclamo
        garantia.estado_garantia = estado_garantia
        garantia.observaciones = observaciones
        garantia.cliente = cliente
        garantia.pedido = pedido
        garantia.save()
        return redirect('lista_garantia')
    return render(request, 'garantia/editar_garantia.html', {'garantia': garantia, 'clientes': Cliente.objects.all(), 'pedidos': Pedido.objects.all()})

def eliminar_garantia(request, id):
    garantia = get_object_or_404(Garantia, id=id)
    garantia.delete()
    return redirect('lista_garantia')
    
