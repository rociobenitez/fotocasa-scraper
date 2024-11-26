import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Mantener el navegador abierto después de que el programa termine
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
)

# Inicializar el webdriver
driver = webdriver.Chrome(options=chrome_options)

# URL de Fotocasa
url = 'https://www.fotocasa.es/es/comprar/pisos/madrid-capital/todas-las-zonas/l?combinedLocationIds=724%2C14%2C28%2C173%2C0%2C28079%2C0%2C176%2C0%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C177%2C142%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C177%2C137%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C681%2C107%3B724%2C14%2C28%2C173%2C0%2C28079%2C0%2C681%2C110&maxPrice=400000&minRooms=2'
driver.get(url)

# Aceptar las cookies
time.sleep(2) # Esperar a que cargue
try:
    cookies_button = driver.find_element(By.ID, 'didomi-notice-agree-button')
    cookies_button.click()
    print("Cookies aceptadas correctamente.")
    time.sleep(2)
except Exception as e:
    print("No se encontró el botón de cookies o no se aceptaron previamente.")

# Lista para almacenar todos los datos
datos_totales = []

while True:
    # Simular scroll para cargar todos los anuncios en la página actual
    prev_num_anuncios = 0
    scroll_attempts = 0
    max_scroll_attempts = 20  # Número máximo de intentos para evitar un bucle infinito

    while scroll_attempts < max_scroll_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))  # Pausa aleatoria
        anuncios_actuales = len(driver.find_elements(By.TAG_NAME, 'article'))
        if anuncios_actuales == prev_num_anuncios:
            break
        prev_num_anuncios = anuncios_actuales
        scroll_attempts += 1

    # Capturar el HTML de la página actual
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    resultados = soup.find('section', class_='re-SearchResult')
    anuncios = resultados.find_all('article') if resultados else []

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
            datos_totales.append({
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
        time.sleep(3)  # Pausa para cargar la nueva página
    except Exception as e:
        print("No hay más páginas disponibles.")
        break

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los datos
df = pd.DataFrame(datos_totales)

# Guardar los datos en un archivo CSV
df.to_csv('pisos_fotocasa.csv', index=False, encoding='utf-8-sig')
print("Datos guardados en 'pisos_fotocasa.csv'")
