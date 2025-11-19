from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Cotizacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def total(self):
        return sum([d.subtotal() for d in self.detallecotizacion_set.all()])

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.nombre}"

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.producto.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"

# === MODELOS DE VENTAS ===
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada')
    ], default='PENDIENTE')

    def total(self):
        return sum([d.subtotal() for d in self.detalleventa_set.all()])

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_venta

    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"