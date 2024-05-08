from .models import Region, Comuna, Direccion, Usuario, Inmueble, Solicitud

###############     CREATE    ################################################################################
# Las regiones y comunas serán ingresadas manualmente desde el panel de control o cargándolas desde un archivo

# Sólo estamos implementando las funciones CREATE que SÍ se utilizarán en el FRONT
def crear_direccion(calle, numero, comuna_nombre, depto=None):
    comuna = Comuna.objects.get(comuna_nombre=comuna_nombre)
    direccion = Direccion.objects.create(calle=calle, numero=numero, depto=depto, comuna=comuna)
    return direccion

def crear_usuario(username, password, first_name, last_name, rut, telefono, tipo_usuario, direccion_id):
    direccion = Direccion.objects.get(pk=direccion_id)
    usuario = Usuario.objects.create(username=username, password=password, first_name=first_name,
                                       last_name=last_name, rut=rut, direccion=direccion, telefono=telefono,
                                       tipo_usuario=tipo_usuario)
    return usuario

def crear_inmueble(inmueble_nombre, descripcion, m2_construidos, m2_terreno, cantidad_estacionamientos,
                   cantidad_habitaciones, cantidad_banios, direccion_id, tipo_inmueble, precio_mensual_arriendo,
                   usuario_arrendador_id):
    direccion = Direccion.objects.get(pk=direccion_id)
    usuario_arrendador = Usuario.objects.get(pk=usuario_arrendador_id)
    inmueble = Inmueble.objects.create(inmueble_nombre=inmueble_nombre, descripcion=descripcion,
                                       m2_construidos=m2_construidos, m2_terreno=m2_terreno,
                                       cantidad_estacionamientos=cantidad_estacionamientos,
                                       cantidad_habitaciones=cantidad_habitaciones, cantidad_banios=cantidad_banios,
                                       direccion=direccion, tipo_inmueble=tipo_inmueble,
                                       precio_mensual_arriendo=precio_mensual_arriendo,
                                       usuario_arrendador=usuario_arrendador)
    return inmueble

def crear_solicitud(usuario_postulante_id, inmueble_id):
    usuario_postulante = Usuario.objects.get(pk=usuario_postulante_id)
    inmueble = Inmueble.objects.get(pk=inmueble_id)
    solicitud = Solicitud.objects.create(usuario_postulante=usuario_postulante, inmueble=inmueble)
    return solicitud

###############     READ      ################################################################################

# Se listarán las regiones comunas, de modo que estén disponibles en para combo box
def listar_regiones():
    return Region.objects.all()

def listar_comunas():
    return Comuna.objects.all()

# Se listarán las direcciones de los usuarios en caso de que deban actualizarlas
def listar_direcciones_usuarios():
    return Direccion.objects.filter(usuario__isnull=False) # Se busca se listen solamente las direcciones asociadas a usuarios

# Se listarán las direcciones de inmuebles
def listar_direcciones_inmuebles():
    return Direccion.objects.filter(inmueble__isnull=False) # Se busca se listen solamente as direcciones asociadas a inmuebles

# Se listarán los inmuebles disponibles y no disponibles
def listar_inmuebles_disponibles():
    return Inmueble.objects.filter(disponibilidad=True) # Disponibles

def listar_inmuebles_no_disponibles():
    return Inmueble.objects.filter(disponibilidad=False) # No disponibles

# Se listarán los inmuebles disponibles en una comuna especificada
def listar_inmuebles_disponibles_comuna(comuna_nombre):    
    inmuebles_disponibles_comuna = Inmueble.objects.filter(direccion__comuna__comuna_nombre=comuna_nombre, disponibilidad=True)
    return inmuebles_disponibles_comuna

# Se listarán solicitudes que correspondan a un usuario arrendador o usuario arrendatario
def listar_solicitudes_usuario(usuario_id, tipo_usuario):
    if tipo_usuario == 'arrendador':
        usuario = Usuario.objects.get(pk=usuario_id)
        return Solicitud.objects.filter(inmueble__usuario_arrendador=usuario)
    elif tipo_usuario == 'arrendatario':
        usuario = Usuario.objects.get(pk=usuario_id)
        return Solicitud.objects.filter(usuario_postulante=usuario)
    else:        
        return None # Manejo de error o no se encuentra
    
###############     UPDATE    ################################################################################

# Permite actualizar los datos del usuario
def actualizar_datos_usuario(usuario_id, **kwargs):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
        for key, value in kwargs.items():
            setattr(usuario, key, value)
        usuario.save()
        return usuario
    except Usuario.DoesNotExist:
        return None

# Permite actualizar direcciones de usuario e inmuebles
def actualizar_datos_direccion(direccion_id, **kwargs):
    try:
        direccion = Direccion.objects.get(pk=direccion_id)
        for key, value in kwargs.items():
            setattr(direccion, key, value)
        direccion.save()
        return direccion
    except Direccion.DoesNotExist:
        return None

# Permite actualizar los datos de un inmueble
def actualizar_datos_inmueble(inmueble_id, **kwargs):
    try:
        inmueble = Inmueble.objects.get(pk=inmueble_id)
        for key, value in kwargs.items():
            setattr(inmueble, key, value)
        inmueble.save()
        return inmueble
    except Inmueble.DoesNotExist:
        return None

# Permite modificar el estado de una solicitud, cambiando su estado de DISPONIBLE a NO DISPONIBLE
def actualizar_datos_solicitud(solicitud_id, estado_solicitud):
    try:
        solicitud = Solicitud.objects.get(pk=solicitud_id)
        solicitud.estado_solicitud = estado_solicitud
        solicitud.save()
        return solicitud
    except Solicitud.DoesNotExist:
        return None
    
###############     DELETE    ################################################################################

##### CONSIDERACIÓN IMPORTANTE: Como todos los modelos están protegidos para el borrado en cascada, es caso de querer eliminación de objetos, se deberá proceder a un borrado, en un orden tal, que permita la acción. Por ejemplo, si quiero eliminar un usuario arrendatario, se deberá proceder al borrado de todas sus solicitudes primero, luego el usuario y finalmente su dirección. Si por el contrario, se quiere borrar un usuario arrendador se deberá borrar primero todas las solicitadas a sus inmuebles, luego los inmuebles, luego el usuario y por último, su dirección.

def eliminar_direccion(direccion_id):
    try:
        direccion = Direccion.objects.get(pk=direccion_id)
        direccion.delete()
        return True
    except Direccion.DoesNotExist:
        return False

def eliminar_usuario(usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.delete()
        return True
    except Usuario.DoesNotExist:
        return False

def eliminar_inmueble(inmueble_id):
    try:
        inmueble = Inmueble.objects.get(pk=inmueble_id)
        inmueble.delete()
        return True
    except Inmueble.DoesNotExist:
        return False

def eliminar_solicitud(solicitud_id):
    try:
        solicitud = Solicitud.objects.get(pk=solicitud_id)
        solicitud.delete()
        return True
    except Solicitud.DoesNotExist:
        return False


#####################################################################################################################################
# Recordar que se omitió el modelo regiones y comunas, ya que se espera estas sean editadas solamente desde el panel de administración o directamente en la DB o con un archivo JSON
#####################################################################################################################################