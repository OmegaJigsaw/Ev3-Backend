from django.shortcuts import render, redirect
from app.models import User
from app.forms import UserForm, LoginForm, CategoriaForm, ProductoForm

# Create your views here.


def inicio(request):
    return render(request, "inicio.html")

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
    return render(request, "login.html", data)

def AdminDashboard(request):
    return render(request, "admin_dashboard.html")

def CrearCategoria(request):
    form = CategoriaForm()
    data = {"form":form}
    return render(request, "crear.html")

def CrearProducto(request):
    form = ProductoForm()
    data = {"form":form}
    return render(request, "crear.html")

