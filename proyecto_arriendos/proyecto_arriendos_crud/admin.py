from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Region, Comuna, Direccion, Usuario, Inmueble, Solicitud

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="regiones.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Nombre de la Región"])
        for region in queryset:
            writer.writerow([region.region_id, region.region_nombre])
        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="comunas.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Nombre de la Comuna", "ID de la Región"])
        for comuna in queryset:
            writer.writerow([comuna.comuna_id, comuna.comuna_nombre, comuna.region.region_id])
        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="direcciones.csv"'
        writer = csv.writer(response)
        writer.writerow(["ID", "Calle", "Número", "Depto", "Comuna", "Fecha de Creación", "Fecha de Modificación"])
        for direccion in queryset:
            writer.writerow([
                direccion.direccion_id,
                direccion.calle,
                direccion.numero,
                direccion.depto,
                direccion.comuna.comuna_nombre,
                direccion.creacion_registro,
                direccion.modificacion_registro
            ])
        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="usuarios.csv"'
        writer = csv.writer(response)
        writer.writerow(["RUT", "Nombres", "Apellidos", "Dirección", "Teléfono", "Correo Electrónico", "Tipo de Usuario", "Fecha de Creación", "Fecha de Modificación"])
        for usuario in queryset:
            writer.writerow([
                usuario.rut,
                usuario.nombres,
                usuario.apellidos,
                usuario.direccion if usuario.direccion else "Sin dirección",
                usuario.telefono,
                usuario.correo_electronico,
                usuario.tipo_usuario,
                usuario.creacion_registro,
                usuario.modificacion_registro
            ])
        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="inmuebles.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID", "Nombre del Inmueble", "Descripción", "Metros Cuadrados Construidos", "Metros Cuadrados de Terreno",
            "Cantidad de Estacionamientos", "Cantidad de Habitaciones", "Cantidad de Baños", "Dirección",
            "Tipo de Inmueble", "Precio Mensual de Arriendo", "Arrendador", "Disponibilidad", "Fecha de Creación", "Fecha de Modificación"
        ])
        for inmueble in queryset:
            direccion = inmueble.direccion if inmueble.direccion else "Sin dirección"
            arrendador = inmueble.usuario_arrendador.rut if inmueble.usuario_arrendador else "Desconocido"
            writer.writerow([
                inmueble.inmueble_id,
                inmueble.inmueble_nombre,
                inmueble.descripcion,
                inmueble.m2_construidos,
                inmueble.m2_terreno,
                inmueble.cantidad_estacionamientos,
                inmueble.cantidad_habitaciones,
                inmueble.cantidad_banios,
                direccion,
                inmueble.tipo_inmueble,
                inmueble.precio_mensual_arriendo,
                arrendador,
                "Disponible" if inmueble.disponibilidad else "Arrendada",
                inmueble.creacion_registro,
                inmueble.modificacion_registro
            ])
        return response

    export_to_csv.short_description = "Exportar a CSV"


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="solicitudes.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID", "Usuario Postulante", "Inmueble", "Estado de Solicitud", "Fecha de Creación", "Fecha de Modificación"
        ])
        for solicitud in queryset:
            writer.writerow([
                solicitud.solicitud_id,
                solicitud.usuario_postulante.rut if solicitud.usuario_postulante else "Desconocido",
                solicitud.inmueble.inmueble_nombre if solicitud.inmueble else "Desconocido",
                "Aceptada" if solicitud.estado_solicitud else "Pendiente",
                solicitud.creacion_registro,
                solicitud.modificacion_registro
            ])
        return response

    export_to_csv.short_description = "Exportar a CSV"

