import json
from .models import Inmueble

'''
# Requerimiento 2. Consultar inmuebles por comuna
def consultar_inmuebles_por_comuna():
    try:
        
            Consulta las comunas que tienen inmuebles asociados
        
            SELECT DISTINCT proyecto_arriendos_crud_comuna.comuna_nombre 
            FROM proyecto_arriendos_crud_comuna 
            INNER JOIN proyecto_arriendos_crud_direccion ON proyecto_arriendos_crud_comuna.id = proyecto_arriendos_crud_direccion.comuna_id 
            INNER JOIN proyecto_arriendos_crud_inmueble ON proyecto_arriendos_crud_direccion.id = proyecto_arriendos_crud_inmueble.direccion_id;
       
        comunas_con_inmuebles = Inmueble.objects.values_list('direccion__comuna__comuna_nombre', flat=True).distinct()

        data = [] # Lista que almacenará la información de la consulta
        
        # Archivo en el que se almacenará la información (se manejan los caracteres especiales)
        with open('inmuebles_por_comuna.txt', 'w', encoding='utf-8') as archivo_texto:

            # Iteración de la consulta obtenida
            for comuna in comunas_con_inmuebles:
                
                archivo_texto.write(f'Comuna: {comuna}\n-----------------------------------------------\n')
                
           
                    Selecciona los objetos inmueble que pertenezcan a las comuna iterada

                    SELECT * 
                    FROM proyecto_arriendos_crud_inmueble 
                    INNER JOIN proyecto_arriendos_crud_direccion ON proyecto_arriendos_crud_inmueble.direccion_id = proyecto_arriendos_crud_direccion.id 
                    INNER JOIN proyecto_arriendos_crud_comuna ON proyecto_arriendos_crud_direccion.comuna_id = proyecto_arriendos_crud_comuna.id 
                    WHERE proyecto_arriendos_crud_comuna.comuna_nombre = 'nombre_comuna' AND proyecto_arriendos_crud_inmueble.disponibilidad = True;                
                   
                inmuebles_comuna = Inmueble.objects.filter(direccion__comuna__comuna_nombre=comuna, disponibilidad=True)
                            
                # Itera los inmuebles de la comuna iterada
                for inmueble in inmuebles_comuna:
                    archivo_texto.write(f'Nombre: {inmueble.inmueble_nombre}\n')
                    archivo_texto.write(f'Descripción: {inmueble.descripcion}\n\n')

                inmuebles_info = [] # Lista para la información de inmuebles

                for inmueble in inmuebles_comuna:                    
                    # Información de un inmueble
                    inmueble_info = {
                        'nombre': inmueble.inmueble_nombre,
                        'descripcion': inmueble.descripcion
                    }
                    inmuebles_info.append(inmueble_info) # Se agrega a la lista
            
                # Agrega a la lista 'data' la información de todos los inmuebles de la comuna
                data[comuna] = inmuebles_info

        # Guarda los datos en formato JSON
        with open('inmuebles_por_comuna.json', 'w') as archivo_json:
            json.dump(data, archivo_json, indent=4, ensure_ascii=False) # Considera caracteres especiales
        
        print("Datos almacenados en 'inmuebles_por_comuna.txt' y en 'inmuebles_por_comuna.json'")

    # Manejo de excepciones
    except Exception as e:
        print(f'Error al realizar la consulta: {e}')
'''

# Requerimiento 2. Consultar inmuebles por comuna
def consultar_inmuebles_por_comuna():
    try:
        
        ''' Selecciona todos los inmuebles disponibles 
        
        SELECT * FROM inmuebles WHERE disponibilidad=True

        '''
        inmuebles = Inmueble.objects.filter(disponibilidad=True)

        # Conjunto que almacenará las comunas de cada inmueble, sin repetirlas y en orden alfabético
        comunas_con_inmuebles = set(inmueble.direccion.comuna.comuna_nombre for inmueble in inmuebles)
        comunas_con_inmuebles = sorted(comunas_con_inmuebles)
        
        data = []  # Cambio: Ahora data es una lista

        with open('inmuebles_por_comuna.txt', 'w', encoding='utf-8') as archivo_texto:
            for comuna in comunas_con_inmuebles:
                archivo_texto.write(f'Comuna: {comuna}\n-----------------------------------------------\n')

                inmuebles_comuna = Inmueble.objects.filter(direccion__comuna__comuna_nombre=comuna, disponibilidad=True)

                inmuebles_info = []

                for inmueble in inmuebles_comuna:
                    archivo_texto.write(f'Nombre: {inmueble.inmueble_nombre}\n')
                    archivo_texto.write(f'Descripción: {inmueble.descripcion}\n\n')

                    inmueble_info = {
                        'nombre': inmueble.inmueble_nombre,
                        'descripcion': inmueble.descripcion
                    }
                    inmuebles_info.append(inmueble_info)

                # Agregamos un diccionario a la lista data con la comuna y sus inmuebles
                data.append({'comuna': comuna, 'inmuebles': inmuebles_info})

        # Escribe la data en un archivo JSON considerando identación y caracteres especiales
        with open('inmuebles_por_comuna.json', 'w') as archivo_json:
            json.dump(data, archivo_json, indent=4, ensure_ascii=False)

        print("Datos almacenados en 'inmuebles_por_comuna.txt' y en 'inmuebles_por_comuna.json'")

    except Exception as e:
        print(f'Error al realizar la consulta: {e}')

# Requerimiento 3. Consultar inmuebles disponibles por región
def consultar_inmuebles_por_region():
    try:
        # Seleccionar todos los inmuebles disponibles
        inmuebles = Inmueble.objects.filter(disponibilidad=True)

        # Conjunto que almacenará las regiones de cada inmueble, sin repetirlas y en orden alfabético
        regiones_con_inmuebles = set(inmueble.direccion.comuna.region.region_nombre for inmueble in inmuebles)
        regiones_con_inmuebles = sorted(regiones_con_inmuebles)

        data = []  # Lista para almacenar los datos

        with open('inmuebles_por_region.txt', 'w', encoding='utf-8') as archivo_texto:
            for region_nombre in regiones_con_inmuebles:
                archivo_texto.write(f'Región: {region_nombre}\n-----------------------------------------------\n')

                # Obtener todos los inmuebles disponibles en la región
                inmuebles_region = Inmueble.objects.filter(direccion__comuna__region__region_nombre=region_nombre, disponibilidad=True)

                inmuebles_info = []

                for inmueble in inmuebles_region:
                    archivo_texto.write(f'Nombre: {inmueble.inmueble_nombre}\n')
                    archivo_texto.write(f'Descripción: {inmueble.descripcion}\n')
                    archivo_texto.write(f'Comuna: {inmueble.direccion.comuna.comuna_nombre}\n\n')

                    inmueble_info = {
                        'nombre': inmueble.inmueble_nombre,
                        'descripcion': inmueble.descripcion,
                        'comuna': inmueble.direccion.comuna.comuna_nombre
                    }
                    inmuebles_info.append(inmueble_info)

                # Agregar la información de los inmuebles de la región a la lista de datos
                data.append({'region': region_nombre, 'inmuebles': inmuebles_info})

        # Escribe la data en un archivo JSON considerando identación y caracteres especiales
        with open('inmuebles_por_region.json', 'w') as archivo_json:
            json.dump(data, archivo_json, indent=4, ensure_ascii=False)

        print("Datos almacenados en 'inmuebles_por_region.txt' y en 'inmuebles_por_region.json'")

    except Exception as e:
        print(f'Error al realizar la consulta: {e}')
