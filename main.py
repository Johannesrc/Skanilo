# Python modules.
import os
import json
import sys


# Función para escanear un directorio y construir una estructura de archivos
def escanear_directorio(directorio, exclusiones):
    """
    Función recursiva para escanear un directorio y construir una estructura de archivos.

    Args:
        directorio (str): Ruta del directorio a escanear.
        exclusiones (list): Lista de patrones de exclusión.

    Returns:
        dict: Estructura de archivos del directorio.
    """
    # Crear la estructura para el directorio actual
    estructura = {}
    estructura['nombre'] = os.path.basename(directorio)

    try:
        if os.path.isdir(directorio):
            estructura['tipo'] = 'directorio'
            estructura['contenido'] = []

            # Obtener la lista de archivos y directorios en el directorio actual
            archivos = [f for f in os.listdir(directorio) if not any(
                pattern in f for pattern in exclusiones)]

            # Recorrer los archivos y directorios y construir la estructura recursivamente
            for nombre in archivos:
                ruta_completa = os.path.join(directorio, nombre)
                # Validar si es un directorio antes de escanearlo
                if os.path.isdir(ruta_completa):
                    estructura['contenido'].append(
                        escanear_directorio(ruta_completa, exclusiones))
                else:
                    estructura['contenido'].append(
                        {'nombre': nombre, 'tipo': 'archivo'})
        else:
            estructura['tipo'] = 'archivo'
    except Exception as e:
        print(f"Error al escanear directorio {directorio}: {e}")

    return estructura
# End escanear_directorio function.


# Función para cargar los patrones de exclusión desde un archivo
def cargar_exclusiones(ruta_archivo):
    """
    Carga los patrones de exclusión desde un archivo si existe.
    Si el archivo no existe, devuelve una lista vacía.

    Args:
        ruta_archivo (str): Ruta del archivo de exclusiones.

    Returns:
        list: Lista de patrones de exclusión si el archivo existe, de lo contrario una lista vacía.
    """
    exclusiones = []
    try:
        with open(ruta_archivo, 'r') as archivo:
            exclusiones = [linea.strip() for linea in archivo if not linea.strip(
            ).startswith('#') and linea.strip() != ""]
    except FileNotFoundError:
        print(
            f"No se encontró el archivo de exclusiones en la ruta: {ruta_archivo}")
    except Exception as e:
        print(
            f"Error al cargar exclusiones desde el archivo {ruta_archivo}: {e}")

    return exclusiones
# End cargar_exclusiones function.


# Función principal del programa
def main():
    # Solicitar al usuario la ruta del directorio a escanear
    directorio_raiz = input('Ingrese la ruta del directorio a escanear: ')

    # Solicitar al usuario la ruta del archivo de exclusiones
    archivo_exclusiones = input(
        'Ingrese la ruta del archivo de exclusiones (o dejar en blanco si no hay): ')

    # Cargar los patrones de exclusión desde el archivo
    exclusiones = cargar_exclusiones(archivo_exclusiones)

    if os.path.exists(directorio_raiz):
        # Escanear el directorio y guardar la estructura en un archivo JSON
        estructura = escanear_directorio(directorio_raiz, exclusiones)
        with open('estructura_archivos.json', 'w') as archivo_json:
            json.dump(estructura, archivo_json, indent=4)
        print('La estructura del sistema de archivos ha sido guardada en "estructura_archivos.json".')
    else:
        print('El directorio especificado no existe.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
