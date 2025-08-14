

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100, null=True, blank=True)
    documento_id = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    correo_electronico = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre_cliente or f"Cliente {self.id}"


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha_pedido = models.DateField(null=True, blank=True)
    producto = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado_pedido = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id}"


class Factura(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_factura = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Factura {self.id}"


class Garantia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    producto = models.CharField(max_length=100, null=True, blank=True)
    motivo_reclamo = models.TextField(null=True, blank=True)
    fecha_reclamo = models.DateField(null=True, blank=True)
    estado_garantia = models.CharField(max_length=30, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Garantía {self.id}"


class ReciboCaja(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_recibo = models.DateField(null=True, blank=True)
    valor_abonado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    forma_pago = models.CharField(max_length=30, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Recibo {self.id}"


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, null=True, blank=True)
    correo = models.EmailField(unique=True, null=True, blank=True)
    contraseña = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_usuario or self.correo or f"Usuario {self.id}"
