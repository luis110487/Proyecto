from django.urls import path
from . import views

urlpatterns = [
    # Login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    
    # Productos
    path('productos/', views.productos, name='productos'),
    path('productos/lista/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Catálogo y carrito
    path('', views.catalogo_productos, name='catalogo_productos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Cotizaciones
    path('cotizaciones/', views.cotizacion_list, name='cotizacion_list'),
    path('cotizaciones/nueva/', views.cotizacion_create, name='cotizacion_create'),
    path('cotizaciones/<int:pk>/', views.cotizacion_detail, name='cotizacion_detail'),
    path('cotizaciones/<int:pk>/editar/', views.cotizacion_update, name='cotizacion_update'),
    path('cotizaciones/<int:pk>/eliminar/', views.cotizacion_delete, name='cotizacion_delete'),
    
    # NUEVAS URLs para manejar productos en cotizaciones
    path('cotizaciones/eliminar-producto/<int:index>/', views.eliminar_producto_cotizacion, name='eliminar_producto_cotizacion'),
    path('cotizaciones/limpiar/', views.limpiar_cotizacion, name='limpiar_cotizacion'),
    path('api/producto/<int:producto_id>/precio/', views.get_producto_precio, name='get_producto_precio'),
    
    
    # Ventas
path('ventas/', views.venta_list, name='venta_list'),
path('ventas/nueva/', views.venta_create, name='venta_create'),
path('ventas/<int:pk>/', views.venta_detail, name='venta_detail'),
path('ventas/<int:pk>/editar/', views.venta_update, name='venta_update'),
path('ventas/<int:pk>/eliminar/', views.venta_delete, name='venta_delete'),
path('ventas/eliminar-producto/<int:index>/', views.eliminar_producto_venta, name='eliminar_producto_venta'),
path('ventas/limpiar/', views.limpiar_venta, name='limpiar_venta'),
]