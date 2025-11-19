from django import forms
from .models import Categoria, Producto, Cliente, Cotizacion, DetalleCotizacion, Venta, DetalleVenta

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones opcionales...'}),
        }

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones opcionales...'}),
        }

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': 1, 'value': 1}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar TODOS los productos (sin filtrar por activo)
        self.fields['producto'].queryset = Producto.objects.all()  # ← SIN filtro

# Formset para múltiples detalles de cotización
DetalleCotizacionFormSet = forms.inlineformset_factory(
    Cotizacion,
    DetalleCotizacion,
    form=DetalleCotizacionForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'observaciones', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones opcionales...'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_venta']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': 1, 'value': 1}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control precio-input', 'step': '0.01', 'min': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()

