from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
###################################################################################################

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_nombre = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.region_nombre
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regiones"
        ordering = ["region_id"]


class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    comuna_nombre = models.CharField(max_length=80, null=False, blank=False)
    region = models.ForeignKey(Region, null=False, blank=False, on_delete=models.PROTECT) #########

    def __str__(self):
        return self.comuna_nombre
    
    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        ordering = ["comuna_nombre"]


class Direccion(models.Model):
    direccion_id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=80, null=False, blank=False)
    numero = models.CharField(max_length=20, null=False, blank=False)
    depto = models.CharField(max_length=20, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, null=False, blank=False, on_delete=models.PROTECT) ##########
    creacion_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificacion_registro = models.DateTimeField(auto_now=True, null=True, blank=True)

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

    rut = models.CharField(max_length=20, primary_key=True)
    nombres = models.CharField(max_length=80, null=False, blank=False)
    apellidos = models.CharField(max_length=80, null=False, blank=False)
    direccion = models.OneToOneField( ##############################################################
        "Direccion",
        related_name="usuario",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
    )
    telefono = models.CharField(max_length=30, null=False, blank=False)
    correo_electronico = models.CharField(max_length=80, null=False, blank=False)
                                                   ####################
    tipo_usuario = models.CharField(max_length=80, choices=TIPO_CHOICES, null=False, blank=False)
    creacion_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificacion_registro = models.DateTimeField(auto_now=True, null=True, blank=True)

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
        return self.rut

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["apellidos"]

    
    '''
    # Para obtener el nombre del grupo al que va a pertenecer el usuario
    def get_group_name(self):
        if self.tipo_usuario == 'arrendatario':
            return 'Arrendatarios'
        elif self.tipo_usuario == 'arrendador':
            return 'Arrendadores'
        else:
            return None
        
    # De acuerdo al tipo de usuario lo agrega al grupo correspondiente o crea el grupo si no existe
    def save(self, *args, **kwargs):
        if not self.pk:
            grupo_name = self.get_group_name()
            if grupo_name:
                grupo, _ = Group.objects.get_or_create(name=grupo_name)
                self.groups.add(grupo)
        super().save(*args, **kwargs)'''
    



''' este es el segundo modelo creado dado un error y HINT
class Arrendatario(Usuario):
    def save(self, *args, **kwargs):
        
        if not self.pk:
            grupo_name = self.get_group_name() 
            if grupo_name:
                grupo, _ = Group.objects.get_or_create(name=grupo_name)            
                self.groups.add(grupo)
        super().save(*args, **kwargs) '''

''' este era el primer modelo para arrendatario y arrendador por separado
class Arrendador(Usuario):
    def save(self, *args, **kwargs):
        # Verifica si el objeto aún no tiene una clave primaria asignada
        if not self.pk:
            # Obtiene o crea el grupo 'Arrendadores'
            grupo_arrendador, _ = Group.objects.get_or_create(name='Arrendadores')
            # Agrega este objeto (Arrendador) al grupo 'Arrendadores'
            self.groups.add(grupo_arrendador)
        # Llama al método 'save' del modelo base (Usuario)
        super().save(*args, **kwargs)'''


class Inmueble(models.Model):
    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]

    inmueble_id = models.AutoField(primary_key=True)
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
    creacion_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificacion_registro = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.inmueble_nombre
    
    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"
        ordering = ["modificacion_registro"]


class Solicitud(models.Model):
    solicitud_id = models.AutoField(primary_key=True)
    usuario_postulante = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.PROTECT) #######################
    inmueble = models.ForeignKey(Inmueble, null=False, blank=False, on_delete=models.PROTECT) ################################
    estado_solicitud = models.BooleanField(default=False) ########## [ aceptada = True] ############
    creacion_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modificacion_registro = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.solicitud_id
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ["modificacion_registro"]

