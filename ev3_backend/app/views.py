from django.contrib import messages
from django.shortcuts import render, redirect
from app.models import Rol, User, Categoria, Producto, Venta
from app.forms import UserForm, LoginForm, CategoriaForm, ProductoForm
from django.contrib.auth import logout


# HOME
def inicio(request):
    carrito = request.session.get("carro", [])
    user_id = request.session.get('user_id', None)
    nombre = request.session.get('nombre', None)
    username = request.session.get('username', None)

    productos = Producto.objects.all()
    categorias_con_producto = Categoria.objects.filter(producto__isnull=False).distinct()
    
    return render(request, "shared/inicio.html",{
        'carrito': carrito,
        'user_id': user_id,
        'nombre': nombre,
        'username': username,
        'productos': productos,
        'categorias': categorias_con_producto,
    })

# CARRO
def RenderCarro(request):
    return render(request, 'user/carro.html')

# DESCRIPCION DEL PRODUCTO (USER)
def RenderDesc(request):
    render(request, 'user/descProducto.html')

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
# Crear Wrapper de permisos
# @admin_required
def AdminDashboard(request):
    return render(request, "admin/indexAdmin.html")

def RenderCategorias(request):
    form = CategoriaForm()
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if (form.is_valid):
            form.save()
            return AdminDashboard(request)     
    categorias = Categoria.objects.all()
    return render(request, "admin/categorias/categorias.html", {'form': form , 'categorias': categorias})

def ActualizarCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid:
            form.save()
        return AdminDashboard(request)
    form = CategoriaForm(instance=categoria)
    categorias = Categoria.objects.all()
    return render(request, "admin/categorias/categorias.html", {'form': form , 'categorias': categorias})

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

def RenderProductos(request):
    form = ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if (form.is_valid):
            form.save()
            return AdminDashboard(request)     
    productos = Producto.objects.all()
    return render(request, "admin/productos/productos.html", {'form': form , 'productos': productos})


def ActualizarProducto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid:
            form.save()
        return AdminDashboard(request)
    form = ProductoForm(instance=producto)
    productos = Producto.objects.all()
    return render(request, "admin/categorias/categorias.html", {'form': form , 'productos': productos})

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

def RenderVentas(request):
    return render(request, 'admin/ventas/ventas.html')

