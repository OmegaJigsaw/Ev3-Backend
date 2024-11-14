from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views as v

urlpatterns = [
    # USER GENERAL
    path("", v.inicio, name="inicio"),
    path("login/", v.login, name="login"),
    path("register/", v.Register, name="register"),
    path("carro/", v.RenderCarro, name="carro"),

    # ADMIN
    path("admin/admin-dashboard/", v.AdminDashboard, name="admin-dashboard"),

    # Categorias
    path("admin/categorias/", v.RenderCategorias, name="categorias"), 
    # path("admin/crear-categoria/", v.CrearCategoria, name="crear-categoria"), 

    # Productos
    path("admin/productos/", v.RenderProductos, name="productos"), 

    # Ventas
    path("admin/ventas/", v.RenderVentas, name="ventas"), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
