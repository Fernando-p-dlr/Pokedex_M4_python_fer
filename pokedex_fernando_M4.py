import os  # Importa el módulo 'os' para la manipulación de archivos y directorios
import requests  # Importa la librería 'requests' para realizar solicitudes HTTP
import json  # Importa el módulo 'json' para trabajar con datos en formato JSON
import matplotlib.pyplot as plt  # Importa matplotlib para mostrar gráficos e imágenes
from PIL import Image  # Importa la clase Image del módulo PIL (Pillow) para manipular imágenes
from io import BytesIO  # Importa BytesIO para trabajar con streams de bytes en memoria

# Función para obtener la información de un Pokémon a partir de su nombre
def obtener_pokemon_info(nombre_pokemon):
    url_base = 'https://pokeapi.co/api/v2/pokemon/'  # URL base de la API de PokeAPI
    url = url_base + nombre_pokemon.lower()  # Construye la URL completa con el nombre del Pokémon

    respuesta = requests.get(url)  # Realiza una solicitud GET a la URL

    # Verifica si la solicitud fue exitosa (código de estado 200)
    if respuesta.status_code == 200:
        data = respuesta.json()  # Convierte la respuesta JSON en un diccionario Python

        # Obtiene la URL de la imagen frontal del Pokémon y sus estadísticas específicas
        imagen = data['sprites']['front_default']
        peso = data['weight']
        tamaño = data['height']
        movimientos = [movimiento['move']['name'] for movimiento in data['moves']]
        habilidades = [habilidad['ability']['name'] for habilidad in data['abilities']]
        tipos = [tipo['type']['name'] for tipo in data['types']]

        # Crea un diccionario con la información del Pokémon
        pokemon_info = {
            'Nombre': nombre_pokemon,
            'Imagen': imagen,
            'Peso': peso,
            'Tamaño': tamaño,
            'Movimientos': movimientos,
            'Habilidades': habilidades,
            'Tipos': tipos
        }

        # Verifica si la carpeta 'pokedex' existe; si no, la crea
        if not os.path.exists('pokedex'):
            os.makedirs('pokedex')

        # Guarda la información del Pokémon en un archivo JSON dentro de la carpeta 'pokedex'
        with open(f'pokedex/{nombre_pokemon.lower()}.json', 'w') as archivo:
            json.dump(pokemon_info, archivo, indent=4)

        # Devuelve la información del Pokémon
        return pokemon_info

    else:
        # Devuelve None si el Pokémon no fue encontrado
        return None

# Función principal del programa
def main():
    nombre_pokemon = input("Introduce el nombre de un Pokémon: ")  # Solicita el nombre de un Pokémon al usuario
    info_pokemon = obtener_pokemon_info(nombre_pokemon)  # Obtiene la información del Pokémon

    if info_pokemon:  # Verifica si se encontró información del Pokémon
        # Muestra la información del Pokémon por consola
        print(f"\nNombre: {info_pokemon['Nombre']}")
        print(f"Imagen: {info_pokemon['Imagen']}")
        print(f"Peso: {info_pokemon['Peso']}")
        print(f"Tamaño: {info_pokemon['Tamaño']}")
        print(f"Movimientos: {', '.join(info_pokemon['Movimientos'])}")
        print(f"Habilidades: {', '.join(info_pokemon['Habilidades'])}")
        print(f"Tipos: {', '.join(info_pokemon['Tipos'])}")

        # Obtiene la imagen del Pokémon a partir de la URL proporcionada
        imagen_url = info_pokemon['Imagen']
        response = requests.get(imagen_url)
        
        if response.status_code == 200:  # Verifica si se pudo obtener la imagen
            imagen = Image.open(BytesIO(response.content))  # Abre la imagen desde el contenido de la respuesta

            # Crea una figura de Matplotlib y muestra la imagen con título y detalles del Pokémon
            plt.figure(figsize=(6, 6))
            plt.imshow(imagen)
            plt.title(f"{info_pokemon['Nombre']}\nTamaño: {info_pokemon['Tamaño']}, Peso: {info_pokemon['Peso']}")
            plt.axis('off')  # Deshabilita los ejes
            plt.show()
        else:
            print("No se pudo obtener la imagen del Pokémon.")
    else:
        print("¡El Pokémon no fue encontrado!")

if __name__ == "__main__":
    main()