from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# USERS
class Rol(models.Model):
    nombre = models.CharField(max_length=20, default='')

class User(models.Model):
    nombre = models.CharField(max_length=30, default='')
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=128, default='')
    rol = models.ForeignKey(Rol, on_delete=models.DO_NOTHING, default=1)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

# PRODUCTOS
class Categoria(models.Model):
    nombre = models.CharField(max_length=20, default='')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre  

class Producto(models.Model):
    nombre = models.CharField(max_length=30, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    stock = models.IntegerField()
    precio_unitario = models.FloatField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre  

# VENTA
class Venta(models.Model):
    fecha = models.DateField()
    total = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    estado = models.BooleanField(default=True)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    subtotal = models.FloatField()