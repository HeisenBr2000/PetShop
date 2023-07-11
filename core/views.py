from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Categoria, Producto, Boleta, Carrito, DetalleBoleta, Bodega, Perfil
from .forms import ProductoForm, BodegaForm, RegistroClienteForm, IngresarForm, PerfilForm
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.contrib import messages
from .tools import eliminar_registro, verificar_eliminar_registro
from core.templatetags.custom_filters import formatear_dinero, formatear_numero
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        registros = Producto.objects.filter(nombre__icontains=buscar).order_by('nombre')
    else:
        registros = Producto.objects.all().order_by('nombre')

    productos = []
    for registro in registros:
        productos.append(obtener_info_producto(registro.id))

    datos = {'productos': productos}
    return render(request, 'core/index.html', datos)


def registrarme(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            perfil = Perfil.objects.create(
                usuario=user,
                tipo_usuario='Cliente',
                rut=form.cleaned_data['rut'],
                direccion=form.cleaned_data['direccion'],
                subscrito=form.cleaned_data['subscrito'],
                imagen=form.cleaned_data['imagen']
            )
            return redirect('ingresar')

    return render(request, 'core/registrarme.html', {'form': form})


def nosotros(request):
    return render(request, 'core/nosotros.html')


def admin_usuarios(request, accion, id):
    if accion == 'eliminar':
        perfil = get_object_or_404(Perfil, id=id)
        usuario = perfil.usuario
        perfil.delete()
        usuario.delete()
        return redirect('admin_usuarios', accion='crear', id=0)

    form = None
    
    if request.method == 'POST':
        if accion == 'crear':
            form = PerfilForm(request.POST, request.FILES)
        elif accion == 'actualizar':
            perfil = get_object_or_404(Perfil, id=id)
            form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios', accion='actualizar', id=id)
    else:
        if accion == 'crear':
            form = PerfilForm()
        elif accion == 'actualizar':
            perfil = get_object_or_404(Perfil, id=id)
            form = PerfilForm(instance=perfil)

    perfiles = Perfil.objects.all()
    return render(request, 'core/admin_usuarios.html', {'form': form, 'perfiles': perfiles})
    


def admin_bodega(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        for _ in range(cantidad):
            Bodega.objects.create(producto=producto)
        
        if cantidad == 1:
            messages.success(
                request, f'Se ha agregado 1 nuevo "{producto.nombre}" a la bodega')
        else:
            messages.success(
                request, f'Se han agregado {cantidad} productos de "{producto.nombre}" a la bodega')

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    return render(request, 'core/admin_bodega.html', {
        'form': BodegaForm(),
        'productos': lista,
    })

def perfil_detalle(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    acciones = perfil.acciones()

    context = {
        'perfil': perfil,
        'acciones': acciones,
    }

    return render(request, 'perfil_detalle.html', context)

def obtener_productos(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Producto.objects.filter(categoria_id=categoria_id)
    data = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'imagen': producto.imagen.url
        } for producto in productos
    ]
    return JsonResponse(data, safe=False)


def eliminar_producto_en_bodega(request, bodega_id):
    nombre_producto = Bodega.objects.get(id=bodega_id).producto.nombre
    eliminado, error = verificar_eliminar_registro(Bodega, bodega_id, True)

    if eliminado:
        messages.success(
            request, f'Se ha eliminado el ID {bodega_id} ({nombre_producto}) de la bodega')
    else:
        messages.error(request, error)

    return redirect(admin_bodega)


def ventas(request):
    boletas = Boleta.objects.all()
    historial = []
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'nom_cliente': f'{boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}',
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'subscrito': 'Sí' if boleta.cliente.subscrito else 'No',
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/ventas.html', {
        'historial': historial
    })


def boleta(request, nro_boleta):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    detalle_boleta = DetalleBoleta.objects.filter(boleta=boleta)
    datos = {
        'boleta': boleta,
        'detalle_boleta': detalle_boleta
    }
    return render(request, 'core/boleta.html', datos)


def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Despachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(ventas)


def ingresar(request):
    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(index)
            messages.error(request, 'La cuenta o la password no son correctos')
    
    return render(request, "core/ingresar.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
    })


def mis_datos_admin(request):
    return render(request, 'core/mis_datos_admin.html')

def misdatos(request):
    return render(request, 'core/misdatos.html')


def miscompras(request):
    usuario = User.objects.get(username=request.user.username)
    perfil = Perfil.objects.get(usuario=usuario)

    boletas = Boleta.objects.filter(cliente=perfil)
    historial = []
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/miscompras.html', {
        'historial': historial
    })


def salir(request):
    logout(request)
    return redirect(index)


def carrito(request):
    detalle_carrito = Carrito.objects.filter(cliente=request.user.perfil)

    total_a_pagar = 0
    for item in detalle_carrito:
        total_a_pagar += item.precio_a_pagar
    monto_sin_iva = int(round(total_a_pagar / 1.19))
    iva = total_a_pagar - monto_sin_iva

    return render(request, 'core/carrito.html', {
        'detalle_carrito': detalle_carrito,
        'monto_sin_iva': monto_sin_iva,
        'iva': iva,
        'total_a_pagar': total_a_pagar,
    })


def eliminar_producto_en_carrito(request, carrito_id):
    Carrito.objects.get(id=carrito_id).delete()

    return redirect(carrito)

def calcular_precios_producto(producto):
    precio_normal = producto.precio
    precio_oferta = producto.precio * (100 - producto.descuento_oferta) / 100
    precio_subscr = producto.precio * (100 - (producto.descuento_oferta + producto.descuento_subscriptor)) / 100
    hay_desc_oferta = producto.descuento_oferta > 0
    hay_desc_subscr = producto.descuento_subscriptor > 0
    return precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr


def agregar_producto_al_carrito(request, producto_id):
    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)

    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(
        producto)

    precio = producto.precio
    descuento_subscriptor = producto.descuento_subscriptor if perfil.subscrito else 0
    descuento_total = producto.descuento_subscriptor + \
        producto.descuento_oferta if perfil.subscrito else producto.descuento_oferta
    precio_a_pagar = precio_subscr if perfil.subscrito else precio_oferta
    descuentos = precio - precio_subscr if perfil.subscrito else precio - precio_oferta

    Carrito.objects.create(
        cliente=perfil,
        producto=producto,
        precio=precio,
        descuento_subscriptor=descuento_subscriptor,
        descuento_oferta=producto.descuento_oferta,
        descuento_total=descuento_total,
        descuentos=descuentos,
        precio_a_pagar=precio_a_pagar
    )

    return redirect('ficha', producto_id)


def ficha(request, producto_id):
    context = obtener_info_producto(producto_id)
    return render(request, 'core/ficha.html', context)


def obtener_info_producto(producto_id):
    producto = Producto.objects.get(id=producto_id)
    stock = Bodega.objects.filter(producto_id=producto_id).exclude(
        detalleboleta__isnull=False).count()

    con_oferta = f'<span class="text-primary"> EN OFERTA {producto.descuento_oferta}% DE DESCUENTO </span>'
    sin_oferta = '<span class="text-success"> DISPONIBLE EN BODEGA </span>'
    agotado = '<span class="text-danger"> AGOTADO </span>'

    if stock == 0:
        estado = agotado
    else:
        estado = sin_oferta if producto.descuento_oferta == 0 else con_oferta

    en_stock = f'En stock: {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"}'

    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen': producto.imagen,
        'html_estado': estado,
        'html_precio': obtener_html_precios_producto(producto),
        'html_stock': en_stock,
    }


def obtener_html_precios_producto(producto):
    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(
        producto)

    normal = f'Normal: {formatear_dinero(precio_normal)}'
    tachar = f'Normal: <span class="text-decoration-line-through"> {formatear_dinero(precio_normal)} </span>'
    oferta = f'Oferta: <span class="text-success"> {formatear_dinero(precio_oferta)} </span>'
    subscr = f'Subscrito: <span class="text-danger"> {formatear_dinero(precio_subscr)} </span>'

    if hay_desc_oferta > 0:
        texto_precio = f'{tachar}<br>{oferta}'
    else:
        texto_precio = normal

    if hay_desc_subscr > 0:
        texto_precio += f'<br>{subscr}'

    return texto_precio


def admin_productos(request, accion, id):
    form = None

    

    if request.method == 'POST':

        if accion == 'crear':
            form = ProductoForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = ProductoForm(request.POST, request.FILES, instance=Producto.objects.get(id=id))

        if form.is_valid():
            producto = form.save()
            form = ProductoForm(instance=producto)
            messages.success(request, f'El producto "{str(producto)}" se logró {accion} correctamente')
            return redirect(admin_productos, 'actualizar', producto.id)
        else:
            messages.error(request, f'No se pudo {accion} el Producto, pues el formulario no pasó las validaciones básicas')
            return redirect(admin_productos, 'actualizar', id)

    if request.method == 'GET':

        if accion == 'crear':
            form = ProductoForm()

        elif accion == 'actualizar':
            form = ProductoForm(instance=Producto.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Producto, id))
            return redirect(admin_productos, 'crear', '0')

    productazos = Producto.objects.all()
    datos = {
        'form': form,
        'productos': productazos
    }
    return render(request, 'core/admin_productos.html', datos)
    


def premio(request):
    return render(request, 'core/premio.html')


def poblar(request):
    poblar_bd()
    return redirect('index')

@login_required
def mis_datos_admin(request):
    perfil = Perfil.objects.get(usuario=request.user)

    context = {
        'perfil': perfil
    }

    return render(request, 'core/mis_datos_admin.html', context)
