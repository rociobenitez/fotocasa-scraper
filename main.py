import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Mantener el navegador abierto después de que el programa termine
chrome_service = Service("/usr/bin/google-chrome")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.binary_location = "/snap/bin/chromium"  # Ubicación del binario de Chromium
chrome_options.add_argument("--headless")              # Ejecutar en modo sin interfaz
chrome_options.add_argument("--no-sandbox")            # Solución para problemas de entorno
chrome_options.add_argument("--disable-dev-shm-usage") # Solución para problemas de memoria compartida
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
)

# Inicializar el webdriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL de Fotocasa
url = 'https://www.fotocasa.es/es/comprar/pisos/madrid-capital/todas-las-zonas/l?combinedLocationIds=724%2C14%2C28%2C173%2C0%2C28079%2C0%2C176%2C0%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C177%2C142%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C177%2C137%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C681%2C107%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C681%2C110&maxPrice=400000&minRooms=2'
driver.get(url)

# Aceptar las cookies
try:
    time.sleep(2) # Esperar a que cargue
    cookies_button = driver.find_element(By.ID, 'didomi-notice-agree-button')
    cookies_button.click()
    print("Cookies aceptadas correctamente.")
    time.sleep(2)
except Exception as e:
    print("No se encontraron cookies o ya fueron aceptadas.")

# Función para realizar un scroll más natural
def scroll_pagina(driver):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    step = random.randint(200, 400)  # Pasos de desplazamiento aleatorios
    
    while current_position < scroll_height:
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(random.uniform(1.5, 3))  # Pausa aleatoria entre scrolls
        scroll_height = driver.execute_script("return document.body.scrollHeight")
    
    print("Scroll completado.")

# Lista para almacenar los datos de todos los anuncios
datos_pisos = []

# Lógica de paginación
while True:
    print(f"Extrayendo anuncios de: {driver.current_url}")
    scroll_pagina(driver)  # Realizar scroll para cargar todos los anuncios
    
    # Obtener el HTML después del scroll
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extraer la sección de resultados
    resultados = soup.find('section', class_='re-SearchResult')
    if not resultados:
        print("No se encontraron más resultados.")
        break
    
    anuncios = resultados.find_all('article')

    # Extraer datos de cada anuncio
    for anuncio in anuncios:
        try:
            # Título y ubicación (combinados)
            titulo_ubicacion_element = anuncio.find('span', class_='re-I18nPropertyTitle')
            if titulo_ubicacion_element:
                titulo_ubicacion = titulo_ubicacion_element.get_text(strip=True)
                if 'en' in titulo_ubicacion:
                    partes = titulo_ubicacion.split('en', 1)
                    titulo = partes[0].strip()  # Ejemplo: "Piso"
                    ubicacion = partes[1].strip()  # Ejemplo: "Castellana"
                else:
                    titulo = titulo_ubicacion  # Caso en que no se pueda dividir
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
            enlace_element = anuncio.find('a', class_='re-CardPackMinimal-slider') or \
                            anuncio.find('a', class_='re-CardPackPremium-carousel') or \
                            anuncio.find('a', class_='re-CardPackBasic-slider') or \
                            anuncio.find('a', class_='re-CardPackAdvance-slider')
            enlace = f"https://www.fotocasa.es{enlace_element['href']}" if enlace_element and enlace_element.get('href') else "Enlace no disponible"

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

    # Verificar si hay más páginas en el paginador
    try:
        next_page = driver.find_element(By.CSS_SELECTOR, '.sui-MoleculePagination-item .sui-AtomButton--neutral')
        next_page_url = next_page.get_attribute('href')
        print(f"Navegando a la siguiente página: {next_page_url}")
        driver.get(next_page_url)
        time.sleep(random.uniform(3, 5))  # Pausa para cargar la nueva página
    except Exception as e:
        print("No hay más páginas disponibles.")
        break

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los datos
df = pd.DataFrame(datos_pisos)

# Guardar los datos en un archivo CSV
df.to_csv('pisos_fotocasa.csv', index=False, encoding='utf-8-sig')
print("Datos guardados en 'pisos_fotocasa.csv'")
