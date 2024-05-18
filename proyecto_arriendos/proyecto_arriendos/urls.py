"""
URL configuration for proyecto_arriendos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from proyecto_arriendos_crud.views import indice, bienvenido, registro, datos_usuario, agregar_inmueble, inmuebles_arrendador, actualizar_inmueble, eliminar_inmueble, buscar_inmuebles_region, buscar_inmuebles_comuna

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indice, name="indice"),
    path('home', indice, name="indice"),
    path('registro', registro, name="registro"),
    path('datos-usuario', datos_usuario, name="datos_usuario"),
    path('bienvenido', bienvenido, name="bienvenido"),
    path('agregar_inmueble', agregar_inmueble, name="agregar_inmueble"),
    path('inmuebles_arrendador', inmuebles_arrendador, name="inmuebles_arrendador"),
    path('actualizar_inmueble/<int:inmueble_id>', actualizar_inmueble, name="actualizar_inmueble"),
    path('eliminar_inmueble/<int:inmueble_id>', eliminar_inmueble, name="eliminar_inmueble"),
    path('buscar_inmuebles_region', buscar_inmuebles_region, name="buscar_inmuebles_region"),
    path('buscar_inmuebles_comuna/<int:region_id>/', buscar_inmuebles_comuna, name="buscar_inmuebles_comuna"),
    path('accounts/', include('django.contrib.auth.urls'))
]
