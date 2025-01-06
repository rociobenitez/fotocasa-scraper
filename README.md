# Fotocasa Scraper 🏠

Este proyecto es un script en Python que utiliza **BeautifulSoup** y **Selenium** para extraer información de propiedades en venta publicadas en [Fotocasa](https://www.fotocasa.es/). El objetivo es obtener datos clave de los anuncios, como título, precio, ubicación, superficie, número de habitaciones, número de baños y enlace al anuncio, y almacenarlos en un archivo CSV.

El código actualmente opera en un archivo HTML descargado para pruebas de scraping, y hay una versión adaptada para combinar Selenium y BeautifulSoup que permite automatizar la navegación y capturar contenido dinámico.

![Web Fotocasa](img/fotocasa-web-macbook.jpg)

## Características

- **Automatización de la navegación**: Interacción con la página mediante Selenium para manejar contenido dinámico y simulación de scroll.
- **Extracción de datos**: Análisis del DOM con BeautifulSoup para capturar:
  - Título del anuncio
  - Precio
  - Ubicación
  - Superficie
  - Habitaciones y baños
  - Enlace al anuncio
- **Salida estructurada**: Los datos extraídos se guardan en un archivo CSV.

## Limitaciones y Consideraciones

**Bloqueos del sitio:**

- Fotocasa puede bloquear el acceso si detecta un uso automatizado (como scrapers).
- Posibles soluciones:
  - Usar un **User-Agent** realista para simular un navegador.
  - Implementar pausas aleatorias y un scroll más natural para evitar patrones repetitivos.
  - Alternar direcciones IP utilizando una VPN o un servicio de proxies.

**Compatibilidad con versiones de Chrome y ChromeDriver:**

- Es fundamental que las versiones de Google Chrome y ChromeDriver sean compatibles.
- Se recomienda verificar las versiones instaladas ejecutando:
  ```bash
  google-chrome --version
  chromedriver --version
  ```
- Si las versiones no coinciden, descarga la versión adecuada de ChromeDriver desde [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
- Para sistemas macOS, asegúrate de otorgar permisos a `chromedriver` en "Seguridad y Privacidad" si aparece un error de verificación de software malicioso.

**Configuraciones adicionales:**

- En el caso de ejecutar el script en GitHub Actions, asegúrate de que las rutas de `chromedriver` y `google-chrome` estén configuradas correctamente.

## Requisitos

- **Python** 3.10 o superior
- **Google Chrome:** Asegúrate de tener instalada la versión más reciente de Google Chrome.
- **ChromeDriver:** Debes descargar e instalar la versión correcta de ChromeDriver que coincida con tu versión de Chrome.
  - Para sistemas Unix/macOS, mueve el binario a `/usr/local/bin`:
  ```bash
  sudo mv chromedriver /usr/local/bin/chromedriver
  ```
  - Verifica que ChromeDriver esté instalado correctamente:
    ```bash
    chromedriver --version
    ```
- **Librerías necesarias**:
  ```bash
  pip install -r requirements.txt
  ```

## Estructura del Proyecto

```plaintext
fotocasa-scraper/
├── .github/
│   └── workflows/
│       └── main.yml         # Configuración para GitHub Actions
├── img                      # Recursos de imágenes
├── main.py                  # Script principal (Selenium y BeautifulSoup)
├── requirements.txt         # Dependencias del proyecto
├── data
|   └── pisos_fotocasa.csv   # CSV generado por el script
└── README.md                # Documentación del proyecto
```

## Ejecución del script en local

1. **Activa el entorno virtual:**

```bash
source .venv/bin/activate
```

2. **Configuración de dependencias:**

```bash
pip install -r requirements.txt
```

3. **Verifica que chromedriver está configurado:**

```bash
chromedriver --version
```

4. **Ejecuta el script:**

```bash
python main.py
```

El script:

- Acepta cookies automáticamente.
- Realiza un scroll simulado para cargar todos los anuncios.
- Navega por las páginas hasta que no haya más resultados.
- Guarda los datos extraídos en un archivo CSV (`data/pisos_fotocasa.csv`).

## Automatización con GitHub Actions

El proyecto está configurado para ejecutarse automáticamente en GitHub Actions, lo que permite realizar scraping sin necesidad de ejecutarlo localmente. Esto es especialmente útil para programar tareas automáticas o recopilar datos de manera regular.

### Configuración del Workflow

El archivo de configuración del workflow se encuentra en `.github/workflows/fotocasa-scraper.yml`. El flujo incluye los siguientes pasos:

1. **Configurar el entorno:**

   - Instala Python y las dependencias necesarias.
   - Configura Google Chrome y ChromeDriver.

2. **Ejecutar el script:**

   - El script se ejecuta automáticamente en el entorno configurado y genera el archivo `data/pisos_fotocasa.csv`.

3. **Programación automática:**
   - El workflow está configurado para ejecutarse automáticamente cada lunes a las 9:00 AM (UTC) mediante el siguiente cron:
     ```yaml
     on:
       schedule:
         - cron: "0 9 * * 1"
     ```

### Cómo Personalizar el Workflow

- Si deseas cambiar la periodicidad del scraping, modifica el cron en `.github/workflows/fotocasa-scraper.yml`.
- Puedes añadir notificaciones o tareas adicionales, como subir los resultados a un repositorio o enviarlos por correo.

## Enlaces de Referencia

- 🔗 [Documentación de Selenium](https://www.selenium.dev/documentation/)
- 🔗 [Documentación de BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- 🔗 [Descargar ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

> [!NOTE]
> Este proyecto es de uso personal y educativo. Fotocasa puede bloquear el acceso a su sitio si detecta patrones automatizados. Asegúrate de respetar los términos de uso del sitio.
