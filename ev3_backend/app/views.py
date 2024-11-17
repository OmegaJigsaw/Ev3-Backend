import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from app.models import DetalleVenta, Rol, User, Categoria, Producto, Venta
from app.forms import UserForm, LoginForm, CategoriaForm, ProductoForm
from django.contrib.auth import logout


#DECORADORES DE SESSION
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id') and request.session.get('rol_user') == 2:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

# HOME
def inicio(request):
    if request.method == 'POST':
        busqueda = request.POST.get('search')
        filtro = Producto.objects.filter(nombre=busqueda)
        if filtro.exists():
            return RenderDesc(request, filtro.first().id)
        else:
            messages.info(request,'No encontrado')
            return redirect('inicio')

    carrito = request.session.get("carrito", [])
    user_id = request.session.get('user_id', None)
    nombre = request.session.get('nombre', None)
    username = request.session.get('username', None)
    rol = request.session.get('rol_user', None)

    categorias_con_producto = Categoria.objects.filter(producto__isnull=False).distinct()
    
    return render(request, "shared/inicio.html",{
        'carrito': carrito,
        'user_id': user_id,
        'nombre': nombre,
        'username': username,
        'categorias': categorias_con_producto,
        'rol_user': rol,
    })

# CARRO
def RenderCarro(request):
    carrito = request.session.get('carrito', [])
    user_id = request.session.get('user_id', None)
    rol = request.session.get('rol_user', None)
    total_carro = sum(item['subtotal'] for item in carrito)
    return render(request, 'user/carro.html', {
        'carrito': carrito, 
        'total': total_carro,
        'user_id': user_id,
        'rol_user': rol,
        })

def AddCarro(request, id):
    producto = Producto.objects.get(id=id)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', [])

    if producto.imagen:
        imagen_producto = producto.imagen.url
    else:
        imagen_producto = ''
    
    for item in carrito:
        if item['id'] == producto.id:
            item['cantidad'] += cantidad
            item['subtotal'] = item['precio'] * item['cantidad']
            break
    else:
        carrito.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'precio': producto.precio_unitario,
            'subtotal': producto.precio_unitario * cantidad,
            'imagen': imagen_producto,
            'descripcion': producto.descripcion
        })
    request.session['carrito'] = carrito 
    return redirect('inicio')

def CantidadCarro(request, id, op):
    carrito = request.session.get('carrito', [])
    producto = Producto.objects.get(id=id)
    for i in carrito:
        if i['id'] == id:
            if op == 'suma':
                if i['cantidad'] < producto.stock:
                    i['cantidad'] += 1 
            elif op == 'resta' and i['cantidad'] > 1:
                i['cantidad'] -= 1
            i['subtotal'] = i['precio'] * i['cantidad']
            break
    request.session['carrito'] = carrito
    return redirect('carro')

def DeleteItemCarro(request, id):
    carrito = request.session.get('carrito', [])
    carrito = [item for item in carrito if item['id'] != id]
    request.session['carrito'] = carrito
    return redirect('carro')  

# REALIZAR VENTA (CARRO)
def Vender(request):
    carrito = request.session.get('carrito', [])
    if carrito:
        try:
            user = User.objects.get(username=request.session.get('username'))
        except User.DoesNotExist:
            messages.error(request, 'Usuario no Encontrado')
        venta = Venta.objects.create(
            usuario=user,
            fecha=datetime.date.today(),
            total=0,
        )
        total_compra = 0
        
        for item in carrito:
            producto = Producto.objects.get(id=item['id'])
            subtotal = item['subtotal']
            total_compra += subtotal
            
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio_momento_venta= producto.precio_unitario,
                subtotal=subtotal
            )
            producto.stock -= item['cantidad']
            producto.save()

        venta.total = total_compra
        venta.save()

        request.session['carrito'] = []
        messages.success(request, 'Compra Realizada, Gracias por su Preferencia')
    else:
        messages.error(request, 'No hay productos en el carrito.')
    return redirect('carro')

# DESCRIPCION DEL PRODUCTO (USER)
def RenderDesc(request, id):
    producto = Producto.objects.get(id=id)
    return render(request, 'user/descProducto.html', {'producto':producto})

# LOGOUT
def Logout(request):
    logout(request)
    return redirect('inicio')

# LOGIN

def login(request):
    if request.method == 'POST':
        login = LoginForm(request.POST)
        if login.is_valid():
            username = login.cleaned_data.get('username')
            password = login.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    request.session['user_id'] = user.id
                    request.session['nombre'] = user.nombre
                    request.session['username'] = user.username
                    request.session['rol_user'] = user.rol.id
                    if user.rol.id == 1:
                        return redirect('inicio')
                    if user.rol.id == 2:
                        return redirect('admin-dashboard')
                else:
                    messages.error(request, 'Credenciales no Validas')
                    return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Usuario no Encontrado')
                return redirect('login')
        else:
            messages.error(request, 'Formulario Invalido')
            return redirect('login')
    login = LoginForm()
    return render(request, "shared/login.html", {'form': login})

# REGISTER
def Register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = Rol.objects.get(id=1)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Error al Registrar')
            return redirect('register')

    register = UserForm()
    return render(request, 'shared/register.html', {'form': register})

# ADMIN VIEWS
@admin_required
def AdminDashboard(request):
    return render(request, "admin/indexAdmin.html")

@admin_required
def RenderCategorias(request):
    form = CategoriaForm()
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria agregada con éxito.')
            return redirect('categorias')     
    categorias = Categoria.objects.all()
    return render(request, "admin/categorias/categorias.html", {'form': form , 'categorias': categorias})

@admin_required
def ActualizarCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
        return redirect('categorias')
    form = CategoriaForm(instance=categoria)
    categorias = Categoria.objects.all()
    return render(request, "admin/categorias/categorias.html", {'form': form , 'categorias': categorias})

@admin_required
def EliminarCategoria(request, id):
        categoria = Categoria.objects.get(id=id)
        if categoria.disponible == True:
            categoria.disponible = False
            categoria.save()
            return RenderCategorias(request)
        else:
            categoria.disponible = True
            categoria.save()
            return RenderCategorias(request)

def BuscarProducto(producto_nombre):
    return Producto.objects.filter(nombre__icontains=producto_nombre)

@admin_required
def RenderProductos(request):
    form = ProductoForm()
    productos = Producto.objects.all()
    if request.method == "POST":
        if 'agregar_btn' in request.POST:
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto agregado con éxito.')
                return redirect('productos') 
            
        elif 'buscar_btn' in request.POST:
            busqueda = request.POST.get('busqueda', '').strip()
            if busqueda:
                productos = BuscarProducto(busqueda)      
                if not productos:
                        messages.info(request, 'No se encontraron productos con ese nombre.')
            else:
                productos = Producto.objects.all() 

    return render(request, "admin/productos/productos.html", {'form': form , 'productos': productos})

@admin_required
def ActualizarProducto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
        return redirect('productos')
    form = ProductoForm(instance=producto)
    productos = Producto.objects.all()
    return render(request, "admin/productos/productos.html", {'form': form , 'productos': productos})

@admin_required
def EliminarProducto(request, id):
        producto = Producto.objects.get(id=id)
        if producto.disponible == True:
            producto.disponible = False
            producto.save()
            return RenderProductos(request)
        else:
            producto.disponible = True
            producto.save()
            return RenderProductos(request)

@admin_required
def RenderVentas(request):
    ventas_generales = Venta.objects.all()
    ventas = Venta.objects.filter(estado=True)
    ganancias_totales = ventas.aggregate(Sum('total'))['total__sum'] or 0
    productos_vendidos = DetalleVenta.objects.values('producto__nombre').annotate(cantidad_vendida=Sum('cantidad')).order_by('-cantidad_vendida')
    producto_mas_vendido = productos_vendidos.first()
    producto_menos_vendido = productos_vendidos.last()
    data = {
        'ventas': ventas,
        'ventas_generales': ventas_generales,
        'ganancias_totales': ganancias_totales,
        'producto_mas_vendido': producto_mas_vendido,
        'producto_menos_vendido': producto_menos_vendido,
    }
    return render(request, 'admin/ventas/ventas.html', data)

@admin_required
def EliminarVenta(request, id):
        venta = Venta.objects.get(id=id)
        if venta.estado == True:
            venta.estado = False
            venta.save()
            return RenderVentas(request)
        else:
            venta.estado = True
            venta.save()
            return RenderVentas(request)

@admin_required
def RenderDetalleVenta(request, id):
    venta = Venta.objects.get(id=id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    data = {"venta": detalles}
    return render(request, 'admin/ventas/detalle.html', data)