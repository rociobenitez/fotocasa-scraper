# Fotocasa Scraper 🏠

Este proyecto es un script en Python que utiliza **BeautifulSoup** y **Selenium** para extraer información de propiedades en venta publicadas en [Fotocasa](https://www.fotocasa.es/). El objetivo es obtener datos clave de los anuncios, como título, precio, ubicación, superficie, número de habitaciones, número de baños y enlace al anuncio, y almacenarlos en un archivo CSV.

El código actualmente opera en un archivo HTML descargado para pruebas de scraping, y hay una versión adaptada para combinar Selenium y BeautifulSoup que permite automatizar la navegación y capturar contenido dinámico.

![Web Fotocasa](img/fotocasa-web-macbook.jpg)

## Características

- Extracción de datos:
  - Título del anuncio
  - Precio
  - Ubicación
  - Superficie
  - Habitaciones y baños
  - Enlace al anuncio
- Guardado de los datos en formato CSV.
- Interacción automatizada con la página (versión con Selenium).

## Requisitos

- Python 3.9+
- Google Chrome y Chromedriver
- Librerías necesarias: `beautifulsoup4 pandas selenium`

  ```bash
  pip install -r requirements.txt
  ```

## Estructura del Proyecto

```plaintext
fotocasa-scraper/
├── fotocasa.html              # Archivo HTML descargado para pruebas con BeautifulSoup
├── main_bs4.py                # Script principal que usa BeautifulSoup
├── main_selenium.py           # Script combinado con Selenium y BeautifulSoup
├── requirements.txt           # Dependencias del proyecto
├── pisos_fotocasa_actualizado.csv  # Salida en formato CSV
└── README.md                  # Documentación del proyecto
```

- **`main_bs4.py`**: Extracción de datos usando un archivo HTML descargado.
- **`main_selenium.py`**: Navegación automatizada con Selenium y análisis de datos con BeautifulSoup.
- **`fotocasa.html`**: Archivo de prueba con HTML descargado.
- **`pisos_fotocasa_actualizado.csv`**: Salida con los datos extraídos.

## Ejecución

### Con BeautifulSoup

```bash
python main_bs4.py
```

- El archivo `main_bs4.py` analiza un archivo HTML descargado y extrae los datos de los anuncios.
- Es útil para pruebas sin realizar solicitudes repetidas al servidor.
- Asegúrate de tener el archivo `fotocasa.html` en el mismo directorio.

### Con Selenium

```bash
python main_selenium.py
```

El archivo `main_selenium.py` usa Selenium para interactuar con la página y capturar el contenido dinámico generado por scroll.

**Funcionalidades Adicionales:**

- **Aceptar Cookies**: Interactúa con el banner de cookies automáticamente.
- **Simulación de Scroll**: Carga todos los anuncios desplazándose por la página.
- **Análisis con BeautifulSoup**: Extrae la información usando la lógica de `main_bs4.py`.

## **Enlaces de Referencia**

- 🔗 [Documentación de Selenium](https://www.selenium.dev/documentation/)
- 🔗 [Documentación de BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Licencia

Este proyecto es de uso educativo. Respeta las condiciones de uso del sitio web Fotocasa.
