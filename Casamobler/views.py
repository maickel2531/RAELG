from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol

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


