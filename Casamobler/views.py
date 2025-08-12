from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def lista_usuarios(request):
    return render(request, 'lista_usuarios.html')

def crear_usuarios(request):
    return render(request, 'crear_usuarios.html')

def editar_usuarios(request , id):
    return render(request, 'editar_usuarios.html')

def eliminar_usuarios(request , id):
    return render(request, 'eliminar_usuarios.html')
