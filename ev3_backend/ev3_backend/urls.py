from django.contrib import admin
from django.urls import path
from app import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", v.inicio, name="inicio"),
    path("login/", v.login, name="login"),
    path("admin-dashboard/", v.AdminDashboard, name="admin-dashboard"),
    path("crear-categoria/", v.CrearCategoria, name="crear-categoria"),
    
]
