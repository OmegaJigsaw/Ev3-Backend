from django.db import models


# USERS
class Rol(models.Model):
    nombre = models.CharField(max_length=20, default='')

class User(models.Model):
    nombre = models.CharField(max_length=30, default='')
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=128, default='')
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING)

# PRODUCTOS
class Categoria(models.Model):
    nombre = models.CharField(max_length=20, default='')

class Producto(models.Model):
    nombre = models.CharField(max_length=30, default='')
    Categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()
    precio_unitario = models.FloatField()
    disponible = models.BooleanField(default=True)

# VENTA
class Venta(models.Model):
    fecha = models.DateField()
    total = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    subtotal = models.FloatField()