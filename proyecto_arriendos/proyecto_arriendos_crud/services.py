from .models import Region, Comuna, Direccion, Usuario, Inmueble, Solicitud
from django.contrib.auth.models import User ######

###############     CREATE    ################################################################################
# Las regiones y comunas serán ingresadas manualmente desde el panel de control o cargándolas desde un archivo

def crear_direccion(self):
    pass

def crear_usuario(self):
    pass

def crear_inmueble(self):
    pass

def crear_solicitud(self):
    pass

###############     READ      ################################################################################

# Se listarán las regiones comunas, de modo que estén disponibles en para combo box
def listar_regiones(self):
    pass

def listar_comunas(self):
    pass

# Se listarán las direcciones de los usuarios en caso de que deban actualizarlas
def listar_direcciones_usuarios(self):
    pass

# Se listarán las direcciones de inmuebles
def listar_direcciones_inmuebles(self):
    pass

# Se listarán los inmuebles disponibles y no disponibles
def listar_inmuebles_disponibles(self):
    pass

def listar_inmuebles_no_disponibles(self):
    pass

# Se listarán solicitudes que correspondan a un usuario arrendador (uno o varios inmuebles diferentes)
def listar_solicitudes_usuario(self):
    pass




 