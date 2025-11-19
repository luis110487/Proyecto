from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Cotizacion, Producto, Categoria, DetalleCotizacion, Venta, DetalleVenta
from .forms import ClienteForm, CotizacionForm, ProductoForm, CategoriaForm, VentaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

# === LOGIN ===
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'ventas/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# === PANEL ADMINISTRADOR ===
@login_required
def admin_dashboard(request):
    # Estadísticas para el dashboard
    total_ventas = Venta.objects.count()
    ventas_hoy = Venta.objects.filter(fecha=timezone.now().date()).count()
    total_cotizaciones = Cotizacion.objects.count()
    total_productos = Producto.objects.count()
    
    return render(request, 'ventas/admin_dashboard.html', {
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
        'total_cotizaciones': total_cotizaciones,
        'total_productos': total_productos,
    })

# === CATEGORÍAS ===
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'ventas/categoria_list.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'ventas/categoria_form.html', {'form': form})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'ventas/categoria_form.html', {'form': form})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'ventas/categoria_confirm_delete.html', {'categoria': categoria})

# === PRODUCTOS ===
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')
    else:
        form = ProductoForm()
    return render(request, 'ventas/agregar_producto.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/lista_productos.html', {'productos': productos})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'ventas/editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'ventas/eliminar_producto.html', {'producto': producto})

@login_required
def productos(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()

    return render(request, 'ventas/productos.html', {
        'form': form,
        'productos': productos
    })

# === CATÁLOGO PÚBLICO ===
def catalogo_productos(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/catalogo_productos.html', {'productos': productos})

# === CLIENTES ===
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    
    return render(request, 'clientes/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente!')
        return redirect('lista_clientes')
    
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

# === CARRITO DE COMPRAS ===
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('catalogo_productos')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for id, cantidad in carrito.items():
        producto = Producto.objects.get(id=id)
        subtotal = producto.precio_unitario * cantidad
        total += subtotal
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
    return render(request, 'ventas/carrito.html', {'items': items, 'total': total})

def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('catalogo_productos')

def checkout(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for id, cantidad in carrito.items():
        producto = Producto.objects.get(id=id)
        subtotal = producto.precio_unitario * cantidad
        total += subtotal
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})

    return render(request, 'ventas/checkout.html', {'items': items, 'total': total})

# === COTIZACIONES ===
@login_required
def cotizacion_list(request):
    cotizaciones = Cotizacion.objects.all().order_by('-fecha')
    return render(request, 'ventas/cotizacion_list.html', {'cotizaciones': cotizaciones})

@login_required
def cotizacion_create(request):
    if request.method == 'POST':
        if 'agregar_producto' in request.POST:
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad', 1)
            
            if producto_id and cantidad:
                productos_cotizacion = request.session.get('productos_cotizacion', [])
                productos_cotizacion.append({
                    'producto_id': int(producto_id),
                    'cantidad': int(cantidad)
                })
                request.session['productos_cotizacion'] = productos_cotizacion
                messages.success(request, 'Producto agregado a la cotización')
            else:
                messages.error(request, 'Seleccione un producto y cantidad')
            
            return redirect('cotizacion_create')
        
        elif 'guardar_cotizacion' in request.POST:
            form = CotizacionForm(request.POST)
            productos_cotizacion = request.session.get('productos_cotizacion', [])
            
            if form.is_valid():
                try:
                    cotizacion = form.save()
                    
                    for item in productos_cotizacion:
                        try:
                            producto = Producto.objects.get(id=item['producto_id'])
                            DetalleCotizacion.objects.create(
                                cotizacion=cotizacion,
                                producto=producto,
                                cantidad=item['cantidad']
                            )
                        except Producto.DoesNotExist:
                            continue
                    
                    request.session['productos_cotizacion'] = []
                    messages.success(request, 'Cotización creada exitosamente!')
                    return redirect('cotizacion_list')
                    
                except Exception as e:
                    messages.error(request, f'Error al crear la cotización: {str(e)}')
            else:
                messages.error(request, 'Por favor corrija los errores en el formulario')
    
    else:
        form = CotizacionForm()
    
    productos = Producto.objects.all()
    productos_cotizacion = request.session.get('productos_cotizacion', [])
    
    items_con_detalles = []
    total_cotizacion = 0
    
    for item in productos_cotizacion:
        try:
            producto = Producto.objects.get(id=item['producto_id'])
            subtotal = producto.precio_unitario * item['cantidad']
            total_cotizacion += subtotal
            
            items_con_detalles.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue
    
    hoy = timezone.now().strftime('%d/%m/%Y')
    
    return render(request, 'ventas/cotizacion_form.html', {
        'form': form,
        'productos': productos,
        'items_cotizacion': items_con_detalles,
        'total_cotizacion': total_cotizacion,
        'titulo': 'Nueva Cotización',
        'hoy': hoy
    })

@login_required
def eliminar_producto_cotizacion(request, index):
    productos_cotizacion = request.session.get('productos_cotizacion', [])
    
    if 0 <= index < len(productos_cotizacion):
        producto_eliminado = productos_cotizacion.pop(index)
        request.session['productos_cotizacion'] = productos_cotizacion
        
        try:
            producto = Producto.objects.get(id=producto_eliminado['producto_id'])
            messages.success(request, f'Producto "{producto.nombre}" eliminado de la cotización')
        except Producto.DoesNotExist:
            messages.success(request, 'Producto eliminado de la cotización')
    
    return redirect('cotizacion_create')

@login_required
def limpiar_cotizacion(request):
    productos_cotizacion = request.session.get('productos_cotizacion', [])
    if productos_cotizacion:
        request.session['productos_cotizacion'] = []
        messages.success(request, 'Todos los productos han sido eliminados de la cotización')
    else:
        messages.info(request, 'No hay productos para limpiar')
    
    return redirect('cotizacion_create')

@login_required
def cotizacion_detail(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    detalles = cotizacion.detallecotizacion_set.all()
    total_manual = sum(detalle.subtotal() for detalle in detalles)
    
    return render(request, 'ventas/cotizacion_detail.html', {
        'cotizacion': cotizacion,
        'detalles': detalles,
        'total_manual': total_manual
    })

@login_required
def cotizacion_update(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cotización actualizada exitosamente!')
                return redirect('cotizacion_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la cotización: {str(e)}')
    else:
        form = CotizacionForm(instance=cotizacion)
    
    hoy = timezone.now().strftime('%d/%m/%Y')
    
    return render(request, 'ventas/cotizacion_edit.html', {
        'form': form,
        'cotizacion': cotizacion,
        'titulo': 'Editar Cotización',
        'hoy': hoy
    })

@login_required
def cotizacion_delete(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        cotizacion_nombre = f"#{cotizacion.id} - {cotizacion.cliente.nombre}"
        cotizacion.delete()
        messages.success(request, f'Cotización {cotizacion_nombre} eliminada exitosamente!')
        return redirect('cotizacion_list')
    return render(request, 'ventas/cotizacion_confirm_delete.html', {'cotizacion': cotizacion})

# === VENTAS ===
@login_required
def venta_list(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/venta_list.html', {'ventas': ventas})

@login_required
def venta_create(request):
    if request.method == 'POST':
        if 'agregar_producto' in request.POST:
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad', 1)
            precio_venta = request.POST.get('precio_venta', 0)
            
            if producto_id and cantidad and precio_venta:
                productos_venta = request.session.get('productos_venta', [])
                productos_venta.append({
                    'producto_id': int(producto_id),
                    'cantidad': int(cantidad),
                    'precio_venta': float(precio_venta)
                })
                request.session['productos_venta'] = productos_venta
                messages.success(request, 'Producto agregado a la venta')
            else:
                messages.error(request, 'Complete todos los campos del producto')
            
            return redirect('venta_create')
        
        elif 'guardar_venta' in request.POST:
            form = VentaForm(request.POST)
            productos_venta = request.session.get('productos_venta', [])
            
            if form.is_valid():
                try:
                    venta = form.save()
                    
                    for item in productos_venta:
                        try:
                            producto = Producto.objects.get(id=item['producto_id'])
                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=producto,
                                cantidad=item['cantidad'],
                                precio_venta=item['precio_venta']
                            )
                            
                            # Actualizar stock del producto
                            producto.stock -= item['cantidad']
                            producto.save()
                            
                        except Producto.DoesNotExist:
                            continue
                    
                    request.session['productos_venta'] = []
                    messages.success(request, 'Venta registrada exitosamente!')
                    return redirect('venta_list')
                    
                except Exception as e:
                    messages.error(request, f'Error al registrar la venta: {str(e)}')
            else:
                messages.error(request, 'Por favor corrija los errores en el formulario')
    
    else:
        form = VentaForm(initial={'estado': 'COMPLETADA'})
    
    productos = Producto.objects.all()
    productos_venta = request.session.get('productos_venta', [])
    
    items_con_detalles = []
    total_venta = 0
    
    for item in productos_venta:
        try:
            producto = Producto.objects.get(id=item['producto_id'])
            subtotal = item['precio_venta'] * item['cantidad']
            total_venta += subtotal
            
            items_con_detalles.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'precio_venta': item['precio_venta'],
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue
    
    hoy = timezone.now().strftime('%d/%m/%Y')
    
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'productos': productos,
        'items_venta': items_con_detalles,
        'total_venta': total_venta,
        'titulo': 'Nueva Venta',
        'hoy': hoy
    })

@login_required
def eliminar_producto_venta(request, index):
    productos_venta = request.session.get('productos_venta', [])
    
    if 0 <= index < len(productos_venta):
        producto_eliminado = productos_venta.pop(index)
        request.session['productos_venta'] = productos_venta
        
        try:
            producto = Producto.objects.get(id=producto_eliminado['producto_id'])
            messages.success(request, f'Producto "{producto.nombre}" eliminado de la venta')
        except Producto.DoesNotExist:
            messages.success(request, 'Producto eliminado de la venta')
    
    return redirect('venta_create')

@login_required
def limpiar_venta(request):
    productos_venta = request.session.get('productos_venta', [])
    if productos_venta:
        request.session['productos_venta'] = []
        messages.success(request, 'Todos los productos han sido eliminados de la venta')
    else:
        messages.info(request, 'No hay productos para limpiar')
    
    return redirect('venta_create')

@login_required
def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalleventa_set.all()
    total_manual = sum(detalle.subtotal() for detalle in detalles)
    
    return render(request, 'ventas/venta_detail.html', {
        'venta': venta,
        'detalles': detalles,
        'total_manual': total_manual
    })

@login_required
def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Venta actualizada exitosamente!')
                return redirect('venta_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la venta: {str(e)}')
    else:
        form = VentaForm(instance=venta)
    
    hoy = timezone.now().strftime('%d/%m/%Y')
    
    return render(request, 'ventas/venta_edit.html', {
        'form': form,
        'venta': venta,
        'titulo': 'Editar Venta',
        'hoy': hoy
    })

@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        # Restaurar stock antes de eliminar
        detalles = venta.detalleventa_set.all()
        for detalle in detalles:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        
        venta_nombre = f"#{venta.id} - {venta.cliente.nombre}"
        venta.delete()
        messages.success(request, f'Venta {venta_nombre} eliminada exitosamente!')
        return redirect('venta_list')
    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})

# === API PARA PRECIOS ===
def get_producto_precio(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({
            'precio': str(producto.precio_unitario),
            'nombre': producto.nombre,
            'descripcion': producto.descripcion or '',
            'stock': producto.stock
        })
    except Producto.DoesNotExist:
        return JsonResponse({'precio': '0.00', 'nombre': '', 'descripcion': '', 'stock': 0})