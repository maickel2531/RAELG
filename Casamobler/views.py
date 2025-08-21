from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol, Cliente, Pedido ,ReciboCaja , Garantia

# Create your views here.
def index(request):
    return render(request, 'index.html')

def lista_usuarios(request):
    return render(request, 'lista_usuarios.html', {'usuarios': Usuario.objects.all()})

def crear_usuarios(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        rol_id = request.POST.get('rol')

        rol = Rol.objects.get(id=rol_id)  

        Usuario.objects.create(
            nombre_usuario=nombre,
            correo=correo,
            contraseña=contraseña,  # ⚠ Hashear en producción
            rol=rol
        )
    
    return render(request, 'crear_usuarios.html', {'roles': Rol.objects.all()})

def eliminar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('lista_usuarios')

def editar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    roles = Rol.objects.all()
    if request.method == 'POST':
        rol=Rol.objects.get(id=request.POST.get('rol'))
        usuario.nombre_usuario = request.POST.get('nombre')
        usuario.correo = request.POST.get('email')
        if request.POST.get('contraseña') != '': 
            usuario.contraseña = request.POST.get('contraseña')  # ⚠ Hashear en producción  # ⚠ Hashear en producción
        usuario.rol = rol
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'editar_usuarios.html', {'usuario': usuario, 'roles': roles})

def crear_cliente(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        documento_id = request.POST.get('documento_id')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo_electronico = request.POST.get('correo_electronico')
        Cliente.objects.create(
            nombre_cliente=nombre_cliente,
            documento_id=documento_id,
            direccion=direccion,
            telefono=telefono,
            correo_electronico=correo_electronico
        )
    return render(request, 'crear_cliente.html')

def lista_cliente(request):
    return render(request, 'lista_cliente.html', {'clientes': Cliente.objects.all()})


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombre_cliente')
        documento_id = request.POST.get('documento_id')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo_electronico = request.POST.get('correo_electronico')
        cliente.nombre_cliente = nombre_cliente
        cliente.documento_id = documento_id
        cliente.direccion = direccion
        cliente.telefono = telefono
        cliente.correo_electronico = correo_electronico
        cliente.save()
        return redirect('lista_cliente')
    return render(request, 'editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_cliente')

def lista_pedido(request):
    return render(request, 'lista_pedido.html', {'pedidos': Pedido.objects.all()})

def crear_pedido(request):
    if request.method == 'POST':
        fecha_pedido = request.POST.get('fecha_pedido')
        producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')
        estado_pedido = request.POST.get('estado_pedido')
        cliente = Cliente.objects.get(id=request.POST.get('cliente'))
        pedido = Pedido.objects.create(
            fecha_pedido=fecha_pedido,
            producto=producto,
            cantidad=cantidad,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            estado_pedido=estado_pedido,
            cliente=cliente
        )
        return redirect('lista_pedido')
    return render(request, 'crear_pedido.html', {'clientes': Cliente.objects.all()})

def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        fecha_pedido = request.POST.get('fecha_pedido')
        producto = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')
        estado_pedido = request.POST.get('estado_pedido')
        cliente = Cliente.objects.get(id=request.POST.get('cliente'))
        pedido.fecha_pedido = fecha_pedido
        pedido.producto = producto
        pedido.cantidad = cantidad
        pedido.valor_unitario = valor_unitario
        pedido.valor_total = valor_total
        pedido.estado_pedido = estado_pedido
        pedido.cliente = cliente
        pedido.save()
        return redirect('lista_pedido')
    return render(request, 'editar_pedido.html', {'pedido': pedido, 'clientes': Cliente.objects.all()})

def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    return redirect('lista_pedido')

def lista_recibo_de_caja(request):
    return render(request, 'lista_recibo_de_caja.html', {'recibos': ReciboCaja.objects.all()})

def crear_recibo_de_caja(request):
    if request.method == "POST":
        pedido_id = request.POST.get("pedido")
        fecha = request.POST.get("fecha_recibo")
        valor = request.POST.get("valor_abonado")
        forma_pago = request.POST.get("forma_pago")
        observaciones = request.POST.get("observaciones")

        pedido = Pedido.objects.get(id=pedido_id)

        ReciboCaja.objects.create(
            pedido=pedido,
            fecha_recibo=fecha,
            valor_abonado=valor,
            forma_pago=forma_pago,
            observaciones=observaciones
        )

        return redirect("lista_recibo_de_caja")

    return render(request, "crear_recibo_de_caja.html", {
        "pedidos": Pedido.objects.all()})

def editar_recibo_de_caja(request, id):
    recibo = ReciboCaja.objects.get(id=id)

    if request.method == "POST":
        recibo.fecha_recibo = request.POST.get("fecha_recibo")
        recibo.valor_abonado = request.POST.get("valor_abonado")
        recibo.forma_pago = request.POST.get("forma_pago")
        recibo.observaciones = request.POST.get("observaciones")

        pedido_id = request.POST.get("pedido")
        recibo.pedido = Pedido.objects.get(id=pedido_id)

        recibo.save()
        return redirect("lista_recibo_de_caja")

    return render(request, "editar_recibo_de_caja.html", {
        "recibo": recibo,
        "pedidos": Pedido.objects.all()})

def eliminar_recibo_de_caja(request, id):
    recibo = get_object_or_404(ReciboCaja, id=id)
    recibo.delete()
    return redirect('lista_recibo_de_caja')

def lista_garantia(request):
    return render(request, 'lista_garantia.html', {'garantias': Garantia.objects.all()})

def crear_garantia(request):
    if request.method == 'POST':
        producto           = request.POST.get('producto')
        motivo_reclamo     = request.POST.get('motivo_reclamo')
        fecha_reclamo      = request.POST.get('fecha_reclamo')
        estado_garantia    = request.POST.get('estado_garantia')
        observaciones      = request.POST.get('observaciones')
        cliente_id         = request.POST.get('cliente')
        pedido_id          = request.POST.get('pedido')  
        cliente            = Cliente.objects.get(id=cliente_id) if cliente_id else None
        pedido             = Pedido.objects.get(id=pedido_id) if pedido_id else None
        
        Garantia.objects.create(
            producto=producto,
            motivo_reclamo=motivo_reclamo,
            fecha_reclamo=fecha_reclamo,
            estado_garantia=estado_garantia,
            observaciones=observaciones,
            cliente=cliente,
            pedido=pedido
        )
    return render(request, 'crear_garantia.html', {'clientes': Cliente.objects.all(), 'pedidos': Pedido.objects.all()})



def editar_garantia(request, id):
    garantia = get_object_or_404(Garantia, id=id)
    if request.method == 'POST':
        prducto            = request.POST.get('producto')
        motivo_reclamo     = request.POST.get('motivo_reclamo')
        fecha_reclamo      = request.POST.get('fecha_reclamo')
        estado_garantia    = request.POST.get('estado_garantia')
        observaciones      = request.POST.get('observaciones')
        cliente_id         = request.POST.get('cliente')
        pedido_id          = request.POST.get('pedido')
        cliente            = Cliente.objects.get(id=cliente_id) if cliente_id else None
        pedido             = Pedido.objects.get(id=pedido_id) if pedido_id else None

        
        garantia.producto           = producto
        garantia.motivo_reclamo     = motivo_reclamo
        garantia.fecha_reclamo      = fecha_reclamo
        garantia.estado_garantia    = estado_garantia
        garantia.observaciones      = observaciones
        garantia.cliente            = cliente
        garantia.pedido             = pedido
        garantia.save()
        return redirect('lista_garantia')
    return render(request, 'editar_garantia.html', {'garantia': garantia, 'clientes': Cliente.objects.all(), 'pedidos': Pedido.objects.all()})


def eliminar_garantia(request, id):
    garantia = get_object_or_404(Garantia, id=id)
    garantia.delete()
    return redirect('lista_garantia')
    

