from django.contrib import admin
from .models import Cotizacion, DetalleCotizacion, Venta, DetalleVenta

class DetalleCotizacionInline(admin.TabularInline):
    model = DetalleCotizacion
    extra = 1

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha', 'total']
    list_filter = ['fecha', 'cliente']
    inlines = [DetalleCotizacionInline]
    search_fields = ['cliente__nombre']

@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'producto', 'cantidad', 'subtotal']
    list_filter = ['producto']
    
    @admin.register(Venta)
    class VentaAdmin(admin.ModelAdmin):
        list_display = ['id', 'cliente', 'fecha', 'estado', 'total']
        list_filter = ['fecha', 'estado', 'cliente']
        search_fields = ['cliente__nombre']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto', 'cantidad', 'precio_venta', 'subtotal']
    list_filter = ['producto']
