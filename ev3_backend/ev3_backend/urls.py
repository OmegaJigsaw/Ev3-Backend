from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views as v

urlpatterns = [
    # USER GENERAL
    path("", v.inicio, name="inicio"),
    path("login/", v.login, name="login"),
    path("logout/", v.Logout, name="logout"),
    path("register/", v.Register, name="register"),
    
    # CARRO
    path("carro/", v.RenderCarro, name="carro"),
    path("carro/add/<int:id>/", v.AddCarro, name="addCarro"),
    path("carro/add/<int:id>/<str:op>/", v.CantidadCarro, name="cantCarro"),
    path("carro/delete/<int:id>/", v.DeleteItemCarro, name="deleteCarro"),
    path("carro/sale/", v.Vender, name="vender"),

    # ADMIN
    path("admin/admin-dashboard/", v.AdminDashboard, name="admin-dashboard"),

    # CATEGORIAS
    path("admin/categorias/", v.RenderCategorias, name="categorias"), 
    path("admin/categorias/eliminar-categorias<int:id>", v.EliminarCategoria, name="eliminar-categorias"),
    path("admin/categorias/actualizar-categorias<int:id>", v.ActualizarCategoria, name="actualizar-categorias"),
    
    # PRODUCTOS
    path("admin/productos/", v.RenderProductos, name="productos"), 
    path("admin/productos/eliminar-productos<int:id>", v.EliminarProducto, name="eliminar-productos"),
    path("admin/productos/actualizar-productos<int:id>", v.ActualizarProducto, name="actualizar-productos"),

    # Ventas
    path("admin/ventas/", v.RenderVentas, name="ventas"), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
