from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
###################################################################################################

class Region(models.Model):
    region_nombre = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.region_nombre
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regiones"
        ordering = ["region_nombre"]


class Comuna(models.Model):
    comuna_nombre = models.CharField(max_length=80, null=False, blank=False)
    region = models.ForeignKey(Region, null=False, blank=False, on_delete=models.PROTECT) #########

    def __str__(self):
        return self.comuna_nombre
    
    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ["comuna_nombre"]


class Direccion(models.Model):
    calle = models.CharField(max_length=80, null=False, blank=False)
    numero = models.CharField(max_length=20, null=False, blank=False)
    depto = models.CharField(max_length=20, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, null=False, blank=False, on_delete=models.PROTECT) ##########
    created_at = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        if self.depto:        
            return f"{self.calle}, {self.numero}, {self.depto}, {self.comuna}"
        else:        
            return f"{self.calle}, {self.numero}, {self.comuna}"

    class Meta:
        verbose_name = "Direccion"
        verbose_name_plural = "Direcciones"
        ordering = ["comuna"]


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador')
    ]

    rut = models.IntegerField(null=False, blank=False)
    # first_name = models.CharField(max_length=150, null=False, blank=False)  ### NO ES NECESARIO DEFINIR, VIENE DADO POR DEFECTO
    # last_name = models.CharField(max_length=150, null=False, blank=False)   ### NO ES NECESARIO DEFINIR, VIENE DADO POR DEFECTO
    direccion = models.OneToOneField( ##############################################################
        "Direccion",
        related_name="usuario",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    telefono = models.CharField(max_length=30, null=False, blank=False)
    # email = models.CharField(max_length=254, null=False, blank=False) ### NO ES NECESARIO DEFINIR, VIENE DADO POR DEFECTO
                                                   ####################
    tipo_usuario = models.CharField(max_length=80, choices=TIPO_CHOICES, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permissions'
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_groups'
    )

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["last_name"]


class Inmueble(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]

    inmueble_nombre = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    m2_construidos = models.IntegerField(null=False, blank=False)
    m2_terreno = models.IntegerField(null=False, blank=False)
    cantidad_estacionamientos = models.IntegerField(null=False, blank=False)
    cantidad_habitaciones = models.IntegerField(null=False, blank=False)
    cantidad_banios = models.IntegerField(null=False, blank=False)
    direccion = models.OneToOneField( ##############################################################
        "Direccion",
        related_name="inmueble",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )                                               ####################
    tipo_inmueble = models.CharField(max_length=80, choices=TIPO_CHOICES, null=False, blank=False)
    precio_mensual_arriendo = models.FloatField(null=False, blank=False)
    usuario_arrendador = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.PROTECT) #######################
    disponibilidad = models.BooleanField(default=True) ############### [ disponible = True ] ######
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.inmueble_nombre
    
    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"
        ordering = ["created_at"]


class Solicitud(models.Model):
    usuario_postulante = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.PROTECT) #######################
    inmueble = models.ForeignKey(Inmueble, null=False, blank=False, on_delete=models.PROTECT) ################################
    estado_solicitud = models.BooleanField(default=False) ########## [ aceptada = True] ############
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Solicitud {self.pk}"
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ["created_at"]
