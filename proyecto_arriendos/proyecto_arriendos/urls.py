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
from proyecto_arriendos_crud.views import indice, bienvenido, registro, datos_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indice, name="indice"),
    path('home', indice, name="indice"),
    path('registro', registro, name="registro"),
    path('datos_usuario', datos_usuario, name="datos_usuario"),
    path('bienvenido', bienvenido, name="bienvenido"),
    path('accounts/', include('django.contrib.auth.urls'))
]
