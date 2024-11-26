from bs4 import BeautifulSoup
import pandas as pd

# Leer el archivo HTML descargado
with open('fotocasa.html', 'r', encoding='utf-8') as file:
    page_source = file.read()

# Analizar el contenido HTML
soup = BeautifulSoup(page_source, 'html.parser')

# Buscar la sección de resultados
resultados = soup.find('section', class_='re-SearchResult')
anuncios = resultados.find_all('article')

# Lista para almacenar los datos
datos_pisos = []

for anuncio in anuncios:
    try:
        # Título y ubicación
        titulo_ubicacion_element = anuncio.find('span', class_='re-I18nPropertyTitle')
        if titulo_ubicacion_element:
            titulo_ubicacion = titulo_ubicacion_element.get_text(strip=True)
            if 'en' in titulo_ubicacion:
                partes = titulo_ubicacion.split('en', 1)
                titulo = partes[0].strip()
                ubicacion = partes[1].strip()
            else:
                titulo = titulo_ubicacion
                ubicacion = "Ubicación no disponible"
        else:
            titulo = "Título no disponible"
            ubicacion = "Ubicación no disponible"

        # Precio
        precio_element = anuncio.find('span', class_='re-CardPrice')
        precio = precio_element.get_text(strip=True) if precio_element else "Precio no disponible"

        # Características adicionales
        ul_caracteristicas = (
            anuncio.find('ul', class_='re-CardFeatures-wrapper') or
            anuncio.find('ul', class_='re-CardFeaturesWithIcons-wrapper')
        )
        superficie = habitaciones = banos = None
        if ul_caracteristicas:
            for li in ul_caracteristicas.find_all('li'):
                texto = li.get_text(strip=True)
                if 'm²' in texto:
                    superficie = texto
                elif 'hab' in texto:
                    habitaciones = texto
                elif 'baño' in texto:
                    banos = texto

        # Enlace al anuncio
        enlace_element = anuncio.find('a', class_='re-CardPackMinimal-info-container') or \
                         anuncio.find('a', class_='re-CardPackBasic-info-container') or \
                         anuncio.find('a', class_='re-CardPackAdvance-info-container')
        enlace = f"https://www.fotocasa.es{enlace_element['href']}" if enlace_element else "Enlace no disponible"

        # Agregar los datos a la lista
        datos_pisos.append({
            'Título': titulo,
            'Precio': precio,
            'Ubicación': ubicacion,
            'Superficie': superficie,
            'Habitaciones': habitaciones,
            'Baños': banos,
            'Enlace': enlace
        })
    except Exception as e:
        print(f"Error al procesar un anuncio: {e}")

# Mostrar resultados
print(datos_pisos)

# Guardar en CSV
df = pd.DataFrame(datos_pisos)
df.to_csv('pisos_fotocasa_actualizado.csv', index=False, encoding='utf-8-sig')
print("Datos guardados en 'pisos_fotocasa_actualizado.csv'")
