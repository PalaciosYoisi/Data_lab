import requests
from bs4 import BeautifulSoup
import time
import logging
import csv  # Importar biblioteca para escribir en CSV
import mysql.connector  # Importar la biblioteca para conectar a la base de datos

# Configurar logging
logging.basicConfig(
    filename='extraccion_productos.log',  # Archivo de logs
    level=logging.INFO,  # Nivel de logging (puedes cambiarlo a DEBUG para más detalle)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de los logs
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato de la fecha
)

# Conexión a la base de datos
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',  # Cambia 'tu_usuario' por tu usuario de MySQL
    password='',  # Cambia 'tu_contraseña' por tu contraseña de MySQL
    database='offcorss_data'
)
db_cursor = db_connection.cursor()

# Función para extraer información de una página específica
def extraer_productos(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    logging.info(f"Solicitando URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error para códigos de respuesta 4xx/5xx

        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.select_one('#gallery-layout-container')

        # Verificar si se encontró el contenedor
        if container:
            items = container.find_all('div', recursive=False)
            logging.info(f"Se encontraron {len(items)} productos en la página.")
            return items  # Retornar los elementos encontrados
        else:
            logging.warning("No se encontró el contenedor de productos.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al obtener la página: {e}")
        return None


# Crear o abrir archivo CSV para escribir los datos
with open('productos_extraccion.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
    # Definir el encabezado
    campos = ['Categoría', 'Página', 'Posición', 'Descripción', 'Precio Normal', 'Precio Descuento', 'Imagen URL',
              'Tallas']

    # Crear el escritor CSV
    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

    # Escribir el encabezado
    escritor_csv.writeheader()

    # Lista de categorías (actualizar el primer enlace)
    categorias_urls = [
        'https://www.offcorss.com/outlet?page=',
        'https://www.offcorss.com/ropa-bebe-nina?page=',
        'https://www.offcorss.com/ropa-bebe-nino?page=',
        'https://www.offcorss.com/ropa-nina?page=',
        'https://www.offcorss.com/ropa-nino?page='
    ]

    # Mapeo de patrones de URL a categorías
    categorias = {
        'ropa-recien-nacido': 'Recién Nacidos',
        'ropa-bebe': 'Bebés',
        'ropa-nina': 'Niñas',
        'ropa-nino': 'Niños',
        'outlet': 'Outlet'
    }

    # Bucle para iterar sobre las categorías
    for categoria in categorias_urls:
        print(f"Extrayendo productos de la categoría: {categoria}")

        # Inicializar el número de página
        pagina = 1

        # Bucle para iterar sobre las páginas de una categoría
        while True:
            logging.info(f"Iniciando extracción de la página {pagina}.")
            print(f"Iniciando extracción de la página {pagina}.")
            time.sleep(5)  # Pausa para evitar sobrecargar el servidor
            url_actual = categoria + str(pagina)
            productos = extraer_productos(url_actual)

            # Si no se encuentran productos, terminamos el bucle
            if not productos:
                logging.info(
                    f"No se encontraron más productos en la página {pagina}. Finalizando extracción para esta categoría.")
                print(
                    f"No se encontraron más productos en la página {pagina}. Finalizando extracción para esta categoría.")
                break

            # Extraer información de cada producto
            for idx, item in enumerate(productos):
                try:
                    # Descripción
                    descripcion = item.select_one('h2').text.strip() if item.select_one(
                        'h2') else "Descripción no disponible"

                    # Precios
                    precios = [p.text.strip().replace('$', '').replace('.', '').replace(',', '.') for p in item.select(
                        'div.offcorss-apps-newsite-1-x-g-vitrinasShelf__infoContainer > div.offcorss-apps-newsite-1-x-g-vitrinasShelfInfocontainer__top > div > p')]

                    if len(precios) > 1:
                        precio_normal = round(float(precios[0]), 2)
                        precio_descuento = round(float(precios[1]), 2)
                    elif len(precios) == 1:
                        precio_normal = round(float(precios[0]), 2)
                        precio_descuento = None  # Sin descuento
                    else:
                        precio_normal = 0.0
                        precio_descuento = None

                    # Imagen del producto (URL)
                    imagen_element = item.select_one(
                        'div.offcorss-apps-newsite-1-x-g-vitrinasShelf__imageContainer.undefined > img')
                    imagen_url = imagen_element['src'] if imagen_element and imagen_element.has_attr(
                        'src') else "Imagen no disponible"

                    # Posición en la página (usamos el índice)
                    posicion = idx + 1

                    # Tallas
                    tallas = item.select(
                        'div.offcorss-apps-newsite-1-x-g-vitrinasShelf__infoContainer > div.offcorss-apps-newsite-1-x-g-vitrinasShelfInfocontainer__bottom > div > div')
                    tallas_texto = [talla.text.strip() for talla in tallas]
                    tallas = ', '.join(tallas_texto) if tallas_texto else "Tallas no disponibles"

                    # Determinar la categoría a partir de la URL
                    categoria_nombre = ""
                    for clave, nombre_categoria in categorias.items():
                        if clave in categoria:
                            categoria_nombre = nombre_categoria
                            break

                    # Log de producto extraído
                    logging.info(
                        f"Producto {posicion} extraído: {descripcion}, {precio_normal}, {precio_descuento}, {imagen_url}, Tallas: {tallas}")
                    print(
                        f"Producto {posicion} extraído: {descripcion}, {precio_normal}, {precio_descuento}, {imagen_url}, Tallas: {tallas}")

                    # Escribir la fila en el archivo CSV
                    escritor_csv.writerow({
                        'Categoría': categoria_nombre,
                        'Página': pagina,
                        'Posición': posicion,
                        'Descripción': descripcion,
                        'Precio Normal': precio_normal,
                        'Precio Descuento': precio_descuento,
                        'Imagen URL': imagen_url,
                        'Tallas': tallas
                    })

                    # Insertar datos en la base de datos
                    db_cursor.execute("""
                        INSERT INTO productos (descripcion, precio_normal, precio_descuento, imagen_url, tallas, categoria) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (descripcion, precio_normal, precio_descuento, imagen_url, tallas, categoria_nombre))
                    db_connection.commit()  # Confirmar la transacción

                except Exception as e:
                    logging.error(f"Error extrayendo el producto {posicion}: {e}")
                    print(f"Error extrayendo el producto {posicion}: {e}")
                    continue

            # Pasar a la siguiente página
            pagina += 1

# Cerrar la conexión a la base de datos
db_cursor.close()
db_connection.close()

logging.info("Extracción completa.")
