from django.urls import path
from .views import index, registrarme, nosotros, admin_productos, admin_usuarios, admin_bodega
from .views import obtener_productos, eliminar_producto_en_bodega, ventas, boleta, ingresar
from .views import misdatos, miscompras, salir, carrito, ficha, mis_datos_admin
from .views import cambiar_estado_boleta, poblar, eliminar_producto_en_carrito, agregar_producto_al_carrito
from . import views


urlpatterns = [
    path('', index, name='index'),
    path('registrarme', registrarme, name='registrarme'),
    path('nosotros', nosotros, name='nosotros'),
    path('admin_productos/<str:accion>/<int:id>/', admin_productos, name='admin_productos'),
    path('admin_usuarios', admin_usuarios, name='admin_usuarios'),
    path('mis_datos_admin', mis_datos_admin, name='mis_datos_admin'),
    path('admin_bodega', admin_bodega, name='admin_bodega'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('eliminar_producto_en_bodega/<int:bodega_id>', eliminar_producto_en_bodega, name='eliminar_producto_en_bodega'),
    path('ventas', ventas, name='ventas'),
    path('boleta/<int:nro_boleta>', boleta, name='boleta'),
    path('cambiar_estado_boleta/<int:nro_boleta>/<str:estado>', cambiar_estado_boleta, name='cambiar_estado_boleta'),
    path('ingresar', ingresar, name='ingresar'),
    path('misdatos', misdatos, name='misdatos'),
    path('miscompras', miscompras, name='miscompras'),
    path('salir', salir, name='salir'),
    path('carrito', carrito, name='carrito'),
    path('eliminar_producto_en_carrito/<int:carrito_id>', eliminar_producto_en_carrito, name='eliminar_producto_en_carrito'),
    path('agregar_producto_al_carrito/<int:producto_id>', agregar_producto_al_carrito, name='agregar_producto_al_carrito'),
    path('ficha/<int:producto_id>', ficha, name='ficha'),
    path('admin_productos', admin_productos, name='admin_productos'),
    path('admin_usuarios', admin_usuarios, name='admin_usuarios'),
    path('salir', salir, name='cerrar_sesion'),
    path('admin_usuarios/<str:accion>/<int:id>/', views.admin_usuarios, name='admin_usuarios'),
    path('mis_datos_admin', mis_datos_admin, name='mis_datos_admin'),
    path('poblar', poblar, name='poblar'),
    path('admin_productos/eliminar/<int:id>/', views.admin_productos, name='eliminar_producto'),
    path('admin_bodega/', views.admin_bodega, name='admin_bodega'),
    
    
]
