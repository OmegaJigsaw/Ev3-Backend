from django.shortcuts import render, redirect
from app.models import User
from app.forms import UserForm, LoginForm, CategoriaForm, ProductoForm

# Create your views here.

# HOME
def inicio(request):
    return render(request, "shared/inicio.html")

# CARRO
def RenderCarro(request):
    return render(request, 'user/carro.html')

# DESCRIPCION DEL PRODUCTO (USER)
def RenderDesc(request):
    render(request, 'user/descProducto.html')

# LOGIN
USERS = {
    'admin': {'password': 'admin', 'redirect': 'admin-dashboard'},
    'usuario': {'password': 'usuario', 'redirect': 'bodeguero_dashboard'},
}

def login(request):
    form = LoginForm()
    data = {"form":form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username in USERS and USERS[username]['password'] == password:
            return redirect(USERS[username]['redirect'])
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, "shared/login.html", data)

# REGISTER
def Register(request):
    return render(request, 'shared/register.html')

# ADMIN VIEWS
# Crear Wrapper de permisos
# @admin_required
def AdminDashboard(request):
    return render(request, "admin/indexAdmin.html")

def RenderCategorias(request):
    return render(request, 'admin/categorias/categorias.html')

def RenderProductos(request):
    return render(request, 'admin/productos/productos.html')

def RenderVentas(request):
    return render(request, 'admin/ventas/ventas.html')

