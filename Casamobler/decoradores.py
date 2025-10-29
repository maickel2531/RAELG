from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def rol_requerido(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            perfil = getattr(request.user, 'perfil', None)
            rol = getattr(perfil, 'rol', None)

            # Si no hay rol, negar acceso y notificar
            if not rol:
                messages.error(request, 'No tienes permisos para acceder al CRUD')
                return redirect('dashboard')

            # Intentar varios nombres de campo comunes en el modelo Rol
            role_name = None
            for attr in ('nombrerol', 'nombre', 'nombre_rol', 'name'):
                role_name = getattr(rol, attr, None)
                if role_name:
                    break

            # Si no se encontró, usar el __str__ del objeto como fallback
            if not role_name:
                role_name = str(rol) if rol else None

            if role_name != required_role:
                messages.error(request, 'No tienes permisos para acceder al CRUD')
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
