from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group

from django.views.generic import TemplateView
from django.views import View

from .models import Region, Comuna, Direccion, Usuario, Inmueble 

# Create your views here.

# Vista de inicio del sitio
def indice(request):
    return render(request, "indice.html", {})

# Vista de redireccionamiento de usuario logeado
def bienvenido(request):

    usuario_personalizado = Usuario.objects.get(user=request.user)
    direccion = usuario_personalizado.direccion

    # Verificar si el usuario pertenece a los grupos de arrendadores o arrendatarios
    pertenece_arrendador = usuario_personalizado.user.groups.filter(name='Arrendadores').exists()
    pertenece_arrendatario = usuario_personalizado.user.groups.filter(name='Arrendatarios').exists()

    contexto = {
        'user': request.user,
        'usuario_personalizado': usuario_personalizado,
        'direccion': direccion,
        'pertenece_arrendador': pertenece_arrendador,
        'pertenece_arrendatario': pertenece_arrendatario
    }

    return render(request, "bienvenido.html", contexto)

def buscar_inmuebles_comuna(request, region_id):

    selected_comuna = None # Comuna seleccionada por defecto
 
    region = get_object_or_404(Region, pk=region_id) 
    comunas = Comuna.objects.filter(region=region) # Obtiene las comunas de la región seleccionada
    # Obtiene los inmuebles de dichas comunas
    inmuebles = Inmueble.objects.filter(direccion__comuna__in=comunas, disponibilidad=True)

    comuna_id = request.GET.get('comuna')

    if comuna_id:
        selected_comuna = get_object_or_404(Comuna, pk=comuna_id) # Selecciona la comuna
        inmuebles = inmuebles.filter(direccion__comuna_id=comuna_id)

    contexto = {
        'region': region,
        'comunas': comunas,
        'inmuebles': inmuebles,
        'selected_comuna': selected_comuna # Pasa la comuna al contexto
    }
    return render(request, "buscar_inmuebles_comuna.html", contexto)

def buscar_inmuebles_region(request):

    selected_region = None # Región seleccionada por defecto

    regiones = Region.objects.all()
    inmuebles = Inmueble.objects.filter(disponibilidad=True)

    region_id = request.GET.get('region')

    if region_id:
        selected_region = get_object_or_404(Region, pk=region_id) # Selecciona la región
        inmuebles = inmuebles.filter(direccion__comuna__region_id=region_id)

    contexto = {
        'regiones': regiones,
        'inmuebles': inmuebles,
        'selected_region': selected_region # pasa la región al contexto de la vista
    }
    return render(request, "buscar_inmuebles_region.html", contexto)

def eliminar_inmueble(request, inmueble_id):

    # Obtener el inmueble por su ID
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id)
    # Obtiene dirección del inmueble
    direccion_inmueble = inmueble.direccion

    inmueble.delete() # Elimina el inmueble
    direccion_inmueble.delete() # Elimina la dirección

    return render(request, "eliminar_inmueble.html", {})


def actualizar_inmueble(request, inmueble_id):
    
    # Obtener el inmueble por su ID
    # inmueble = Inmueble.objects.get(pk=inmueble_id)

    # Obtener el inmueble por su ID
    inmueble = get_object_or_404(Inmueble, pk=inmueble_id)

    # Obtener todas las comunas
    comunas = Comuna.objects.all()

    if request.method == 'POST':

        # Actualizar datos del inmueble
        inmueble.inmueble_nombre = request.POST.get('inmueble_nombre', inmueble.inmueble_nombre)
        inmueble.descripcion = request.POST.get('descripcion', inmueble.descripcion)
        inmueble.m2_construidos = request.POST.get('m2_construidos', inmueble.m2_construidos)
        inmueble.m2_terreno = request.POST.get('m2_terreno', inmueble.m2_terreno)
        inmueble.cantidad_estacionamientos = request.POST.get('cantidad_estacionamientos', inmueble.cantidad_estacionamientos)
        inmueble.cantidad_habitaciones = request.POST.get('cantidad_habitaciones', inmueble.cantidad_habitaciones)
        inmueble.cantidad_banios = request.POST.get('cantidad_banios', inmueble.cantidad_banios)

        inmueble.precio_mensual_arriendo = request.POST.get('precio_mensual_arriendo', inmueble.precio_mensual_arriendo)
        inmueble.tipo_inmueble = request.POST.get('tipo_inmueble', inmueble.tipo_inmueble)
        
        inmueble.save() # guarda los cambios en el inmueble               

        # Actualizar la dirección
        inmueble.direccion.calle = request.POST.get('calle', inmueble.direccion.calle)
        inmueble.direccion.numero = request.POST.get('numero', inmueble.direccion.numero)
        inmueble.direccion.depto = request.POST.get('depto', inmueble.direccion.depto)
        inmueble.direccion.comuna_id = request.POST.get('comuna', inmueble.direccion.comuna_id)
        
        inmueble.direccion.save() # guarda los cambios en la dirección

        return redirect('inmuebles_arrendador')

    contexto = {
        'inmueble': inmueble,        
        'comunas': comunas
    }

    return render(request, "actualizar_inmueble.html", contexto)

# Vista para desplegar los inmuebles de un arrendador, con opción a eliminar o actualizar
def inmuebles_arrendador(request):

    # Obtener el usuario actualmente autenticado
    usuario_arrendador = Usuario.objects.get(user=request.user)

    # Obtener los inmuebles del usuario arrendador
    inmuebles_arrendador = Inmueble.objects.filter(usuario_arrendador=usuario_arrendador, disponibilidad=True)
    
    return render(request, 'inmuebles_arrendador.html', {'inmuebles_arrendador': inmuebles_arrendador})        

# Vista para agregar inmueble
def agregar_inmueble(request):
    comunas = Comuna.objects.all() # Obtiene todas las comunas

    if request.method == 'POST':
        # Extraer datos del formulario de dirección
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        depto = request.POST.get('depto')
        comuna_id = request.POST.get('comuna')

        # Crear una nueva dirección
        nueva_direccion = Direccion.objects.create(
            calle=calle,
            numero=numero,
            depto=depto,
            comuna_id=comuna_id
        )

        # Guardar la nueva dirección en la base de datos
        nueva_direccion.save()

        # Extraer datos del formulario de inmueble
        inmueble_nombre = request.POST.get('inmueble_nombre')
        descripcion = request.POST.get('descripcion')
        m2_construidos = request.POST.get('m2_construidos')
        m2_terreno = request.POST.get('m2_terreno')
        cantidad_estacionamientos = request.POST.get('cantidad_estacionamientos')
        cantidad_habitaciones = request.POST.get('cantidad_habitaciones')
        cantidad_banios = request.POST.get('cantidad_banios')
        tipo_inmueble = request.POST.get('tipo_inmueble')
        precio_mensual_arriendo = request.POST.get('precio_mensual_arriendo')
        usuario_arrendador = Usuario.objects.get(user=request.user)

        # Crear un nuevo inmueble y asignar la dirección creada
        nuevo_inmueble = Inmueble.objects.create(
            inmueble_nombre=inmueble_nombre,
            descripcion=descripcion,
            m2_construidos=m2_construidos,
            m2_terreno=m2_terreno,
            cantidad_estacionamientos=cantidad_estacionamientos,
            cantidad_habitaciones=cantidad_habitaciones,
            cantidad_banios=cantidad_banios,
            direccion=nueva_direccion,
            tipo_inmueble=tipo_inmueble,
            precio_mensual_arriendo=precio_mensual_arriendo,
            usuario_arrendador=usuario_arrendador,
            disponibilidad=True
        )

        # Guardar el nuevo inmueble en la base de datos
        nuevo_inmueble.save()

        return redirect('bienvenido')

    return render(request, 'agregar_inmueble.html', {'comunas': comunas})

# Vista de actualización de datos de usuario
def datos_usuario(request):

    usuario_personalizado = Usuario.objects.get(user=request.user)
    direccion = usuario_personalizado.direccion
    comunas = Comuna.objects.all()
    
    if request.method == 'POST':

        # Actualizar datos del usuario
        usuario_personalizado.user.username = request.POST.get('username', usuario_personalizado.user.username)
        # No se trabaja con contraseña
        
        usuario_personalizado.user.first_name = request.POST.get('first_name', usuario_personalizado.user.first_name)
        usuario_personalizado.first_name = request.POST.get('first_name', usuario_personalizado.user.first_name)
        
        usuario_personalizado.user.last_name = request.POST.get('last_name', usuario_personalizado.user.last_name)
        usuario_personalizado.last_name = request.POST.get('last_name', usuario_personalizado.user.last_name)

        usuario_personalizado.user.email = request.POST.get('email', usuario_personalizado.user.email)
        usuario_personalizado.email = request.POST.get('email', usuario_personalizado.user.email)

        usuario_personalizado.user.save()        

        # Actualizar datos del usuario personalizado
        usuario_personalizado.telefono = request.POST.get('telefono', usuario_personalizado.telefono)
        usuario_personalizado.tipo_usuario = request.POST.get('tipo_usuario', usuario_personalizado.tipo_usuario)
        usuario_personalizado.save()

        # Asignar el usuario al grupo correspondiente según tipo_usuario
        if usuario_personalizado.tipo_usuario == 'arrendatario':
            grupo = Group.objects.get(name='Arrendatarios')
        elif usuario_personalizado.tipo_usuario == 'arrendador':
            grupo = Group.objects.get(name='Arrendadores')
        else:
            grupo = None

        if grupo:
            usuario_personalizado.user.groups.clear()  # Limpiar todos los grupos actuales en ambas tablas
            usuario_personalizado.groups.clear()

            usuario_personalizado.user.groups.add(grupo) # Agrega al usuario al grupo correspondiente
            usuario_personalizado.groups.add(grupo)

        # Actualizar la dirección
        direccion.calle = request.POST.get('calle', direccion.calle)
        direccion.numero = request.POST.get('numero', direccion.numero)
        direccion.depto = request.POST.get('depto', direccion.depto)  # Departamento es opcional
        direccion.comuna_id = request.POST.get('comuna', direccion.comuna_id)
        direccion.save()

        return redirect('bienvenido')

    return render(request, 'datos_usuario.html', {'usuario_personalizado': usuario_personalizado, 'comunas': comunas})

# Vista de registro de usuario
def registro(request):

    comunas = Comuna.objects.all() # Trae todas las comunas desde la DB

    if request.method == 'POST':

        # Extraer datos del formulario de dirección
        calle = request.POST.get('calle')
        numero = request.POST.get('numero')
        depto = request.POST.get('depto')
        comuna_id = request.POST.get('comuna')

        # Crear una nueva dirección
        nueva_direccion = Direccion.objects.create(
            calle=calle,
            numero=numero,
            depto=depto,
            comuna_id=comuna_id
        )

        # Guardar la nueva dirección en la base de datos
        nueva_direccion.save()
        
        # Extraer datos del formulario de dirección
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rut = request.POST.get('rut')        
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        tipo_usuario = request.POST.get('tipo_usuario')

        # Crear un nuevo usuario (auth_user) y asignar la dirección creada
        nuevo_usuario = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        nuevo_usuario.save()     # Guarda al usuario en la tabla auth_user
        
        # Crear un nuevo usuario y asignar la dirección creada
        nuevo_usuario_personalizado = Usuario.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            rut=rut,
            direccion=nueva_direccion,
            email=email,
            telefono=telefono,
            tipo_usuario=tipo_usuario,
            user=nuevo_usuario            
        )
                        
        nuevo_usuario_personalizado.save()      # Guarda al usuario en la tabla personalizada Usuario

        # Asignar el usuario al grupo correspondiente según tipo_usuario
        if tipo_usuario == 'arrendatario':
            grupo = Group.objects.get(name='Arrendatarios')
        elif tipo_usuario == 'arrendador':
            grupo = Group.objects.get(name='Arrendadores')
        else:
            grupo = None # No pertenece a ninguno

        if grupo:
            nuevo_usuario.groups.add(grupo) # Si se le asigna grupo al usuario, entonces se agrega al grupo

        return redirect('indice')
    else:
        return render(request, "registro.html", {'comunas': comunas})
    

class LoginRequiredMixin(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Welcome(LoginRequiredMixin, TemplateView):
    template_name = "bienvenido.html"
    