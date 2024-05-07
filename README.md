# Proyecto: Manejo del CRUD - Arriendo de Inmuebles

## Descripción

Este proyecto consiste en la creación de un sitio web dedicado al arriendo de inmuebles, donde los usuarios pueden buscar propiedades disponibles para arrendar, separadas por comuna y región. El sitio web cuenta con dos tipos de usuarios: arrendatarios y arrendadores, cada uno con funcionalidades específicas.

## Modelo Entidad-Relación

El archivo [proyecto_arriendos.jpg](proyecto_arriendos.jpg) contiene el modelo entidad-relación físico de la base de datos del proyecto. Este archivo muestra la estructura de las tablas y las relaciones entre ellas, lo que proporciona una visión clara de cómo se organizarán y almacenarán los datos en el sistema.

## Datos de Prueba

Para poblar la base de datos con datos de prueba, se proporciona un archivo JSON llamado `datos_prueba.json`. Puedes cargar estos datos utilizando el comando `loaddata` de Django:

```bash
python manage.py loaddata datos_prueba.json
```

Esto insertará los registros de prueba en la base de datos y te permitirá comenzar a explorar la aplicación con datos preexistentes.

## Hitos

El proyecto está dividido en 5 etapas:

### Registro de usuarios y gestión de datos básicos

En este primer hito del proyecto, se establece la base para el desarrollo del sitio web de arriendo de inmuebles. Se configura el entorno de desarrollo integrado por Django y PostgreSQL, asegurando que el ambiente cuente con todas las herramientas necesarias para la creación del proyecto. Además, se define el modelo de datos utilizando el framework Django, representando el modelo relacional de la base de datos y estableciendo la conexión con PostgreSQL. Se implementan operaciones CRUD en los modelos para la manipulación de datos, permitiendo la creación, lectura, actualización y eliminación de registros dentro del sistema. Este hito sienta las bases técnicas necesarias para la construcción de la aplicación y garantiza que el proyecto esté listo para avanzar a etapas posteriores.

### Funcionalidades para usuarios tipo arrendatario

completar

### Funcionalidades para usuarios tipo arrendador

completar

### Implementación de vistas y formularios

completar

### Integración y pruebas finales

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
