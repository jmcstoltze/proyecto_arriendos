from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.views.generic import TemplateView
from django.views import View

from .models import Usuario, Comuna, Direccion

# Create your views here.

'''
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bienvenido')  # Redirige a la página de bienvenida después del inicio de sesión exitoso
        else:
            # Usuario no válido, puedes manejar esto de varias maneras, por ejemplo, mostrando un mensaje de error
            return render(request, 'registration/login.html', {'error': 'Nombre de usuario o contraseña incorrectos'})
    else:
        return render(request, "registration/login.html", {})'''


def indice(request):

    # Lógica a implementar

    return render(request, "indice.html", {})

def bienvenido(request):

    usuario_personalizado = Usuario.objects.get(user=request.user)
    direccion = usuario_personalizado.direccion

    contexto = {
        'user': request.user,
        'usuario_personalizado': usuario_personalizado,
        'direccion': direccion
    }

    return render(request, "bienvenido.html", contexto)

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

        # Actualizar la dirección
        direccion.calle = request.POST.get('calle', direccion.calle)
        direccion.numero = request.POST.get('numero', direccion.numero)
        direccion.depto = request.POST.get('depto', direccion.depto)  # Departamento es opcional
        direccion.comuna_id = request.POST.get('comuna', direccion.comuna_id)
        direccion.save()

        return redirect('bienvenido')

    return render(request, 'datos_usuario.html', {'usuario_personalizado': usuario_personalizado, 'comunas': comunas})

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

        return redirect('indice')
    else:
        return render(request, "registro.html", {'comunas': comunas})
    

class LoginRequiredMixin(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Welcome(LoginRequiredMixin, TemplateView):
    template_name = "bienvenido.html"
    