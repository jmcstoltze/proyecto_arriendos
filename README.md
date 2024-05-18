# Proyecto: Manejo del CRUD - Arriendo de Inmuebles

## Descripción

Este proyecto consiste en la creación de un sitio web dedicado al arriendo de inmuebles, donde los usuarios pueden buscar propiedades disponibles para arrendar, separadas por comuna y región. El sitio web cuenta con dos tipos de usuarios: arrendatarios y arrendadores, cada uno con funcionalidades específicas.

## Modelo Entidad-Relación

El archivo [proyecto_arriendos.jpg](proyecto_arriendos.jpg) contiene el modelo entidad-relación físico de la base de datos del proyecto. Este archivo muestra la estructura de las tablas y las relaciones entre ellas, lo que proporciona una visión clara de cómo se organizarán y almacenarán los datos en el sistema.

## Hitos

El proyecto está dividido en 5 etapas:

### 1. Registro de usuarios y gestión de datos básicos

En este primer hito del proyecto, se establece la base para el desarrollo del sitio web de arriendo de inmuebles. Se configura el entorno de desarrollo integrado por Django y PostgreSQL, asegurando que el ambiente cuente con todas las herramientas necesarias para la creación del proyecto. Además, se define el modelo de datos utilizando el framework Django, representando el modelo relacional de la base de datos y estableciendo la conexión con PostgreSQL. Se implementan operaciones CRUD en los modelos para la manipulación de datos, permitiendo la creación, lectura, actualización y eliminación de registros dentro del sistema. Este hito sienta las bases técnicas necesarias para la construcción de la aplicación y garantiza que el proyecto esté listo para avanzar a etapas posteriores.

### 2. Funcionalidades para poblar las tablas del modelo y realizar consultas

Para poblar la base de datos con datos de prueba, se proporciona varios archivos JSON llamados `datos_regiones.json`, `datos_comunas.json`, `datos_direcciones.json`, `datos_usuarios.json`, `datos_inmuebles.json`, `datos_solicitudes.json`. Puedes cargar estos datos utilizando el comando `loaddata` de Django:

```bash
python manage.py loaddata datos_regiones.json
python manage.py loaddata datos_comunas.json
python manage.py loaddata datos_direcciones.json
python manage.py loaddata datos_usuarios.json
python manage.py loaddata datos_inmuebles.json
python manage.py loaddata datos_solicitudes.json
```

Además existen 2 funciones en el archivo `scripts.py`, ubicado en la carpeta de la apliación. Dichas funciones retornarán los inmuebles disponibles, tanto por comuna como por región. Las consultas realizadas con el ORM de Django se almacenan automáticamente en los archivos `consultar_inmuebles_por_comuna.json`, `consultar_inmuebles_por_comuna.txt`, `consultar_inmuebles_por_region.json` y `consultar_inmuebles_por_region.txt`, los cuales quedan disponibles en la carpeta raíz del proyecto.

```bash
python manage.py shell
from nombre_de_tu_app.scripts import consultar_inmuebles_por_comuna, consultar_inmuebles_por_region
python manage.py loaddata datos_comunas.json
```

### 3. Funcionalidades para usuarios tipo arrendador y arrendatario

Se implementan vistas de registro y actualización de información de usuario, previamente implementada la opción de iniciar sesión en la página.

### 4. Implementación de vistas y formularios

- Usuarios 'arrendadores' y 'arrendatarios' son asignados automáticamente al grupo correspondiente en el panel de admnistración.
- Usuarios 'arrendadores' pueden agregar, listar, actualizar y borrar inmuebles. Se implementan las vistas, rutas, funciones y formularios necesarios.
- Usuarios 'arrendatarios' pueden ver ofertas disponibles, listándolas por región y/o comuna.
- Se adjuntan pantallazos del proceso y ejemplos en la carpeta `screenshots`, en la raíz del proyecto.

### 5. Integración y pruebas finales

completar

## Requerimientos de Instalación

Los requerimientos se detallan en el archivo requirements.txt. Incluyen:

- Python 3.10.10
- Django 4.2.11
- Psycopg2

## Configuración del Proyecto

1. Clonar el repositorio
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Configurar la base de datos según las especificaciones del proyecto.
4. Realizar las migraciones de la base de datos
    `python manage.py makemigrations`
    `python manage.py migrate`
5. Iniciar el servidor local: `python manage.py runserver`

## Uso

1. Registrarse como usuario en la aplicación.
2. Iniciar sesión con las credenciales proporcionadas.
3. Explorar las propiedades disponibles según la comuna y región.
4. Para arrendatarios: generar solicitudes de arriendo a las propiedades deseadas.
5. Para arrendadores: publicar nuevas propiedades, listar propiedades existentes, editar o eliminar propiedades, aceptar arrendatarios.

## Autor

Jose Contreras Stoltze
