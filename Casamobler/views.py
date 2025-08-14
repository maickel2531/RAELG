from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol

# Create your views here.
def index(request):
    return render(request, 'index.html')

def lista_usuarios(request):
    usuarios = Usuario.objects.select_related('rol').all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})

def crear_usuarios(request):
    roles = Rol.objects.all()
    if request.method == 'POST':
        Usuario.objects.create(
            nombre_usuario=request.POST['nombre_usuario'],
            correo=request.POST['correo'],
            contraseña=request.POST['contraseña'],  # ⚠ Hashear en producción
            estado=request.POST['estado'],
            rol_id=request.POST['rol']
        )
        return redirect('lista_usuarios')
    return render(request, 'crear_usuarios.html', {'roles': roles})

def editar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    roles = Rol.objects.all()
    if request.method == 'POST':
        usuario.nombre_usuario = request.POST['nombre_usuario']
        usuario.correo = request.POST['correo']
        usuario.contraseña = request.POST['contraseña']  # ⚠ Hashear en producción
        usuario.estado = request.POST['estado']
        usuario.rol_id = request.POST['rol']
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'editar_usuarios.html', {'usuario': usuario, 'roles': roles})

def eliminar_usuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('lista_usuarios')
