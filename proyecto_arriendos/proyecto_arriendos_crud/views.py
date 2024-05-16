from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

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

    # Lógica a implementar

    return render(request, "bienvenido.html", {})

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
        
        # Crear un nuevo usuario y asignar la dirección creada
        nuevo_usuario = Usuario.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            rut=rut,
            direccion=nueva_direccion,
            email=email,
            telefono=telefono,
            tipo_usuario=tipo_usuario
        )

        nuevo_usuario.save()

        return redirect('indice')
    else:
        return render(request, "registro.html", {'comunas': comunas})
    

class LoginRequiredMixin(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Welcome(LoginRequiredMixin, TemplateView):
    template_name = "bienvenido.html"
    