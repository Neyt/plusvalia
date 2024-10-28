import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración de las opciones de Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ejecutar en modo headless (quitar para ver la interfaz gráfica)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU
chrome_options.add_argument("--window-size=1920,1080")  # Tamaño de ventana
chrome_options.add_argument("--ignore-certificate-errors")

# Inicializar el driver de Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Navegar a la página de Plusvalía para locales comerciales en alquiler en Quito
    driver.get("https://www.plusvalia.com/")
    time.sleep(5)  # Esperar un momento para evitar detección de bot
    print(f"Título de la página: {driver.title}")

    # Imprimir el HTML para revisar la estructura
    page_source = driver.page_source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    print("HTML de la página guardado en 'page_source.html' para inspección manual.")

    # Esperar a que los elementos carguen
    wait = WebDriverWait(driver, 20)  # Aumentar el tiempo de espera

    # Ejemplo: Obtener información de un listado
    titles = []
    prices = []

    # Esperar a que carguen los listados y obtener información
    try:
        # Verificar selectores y ajustarlos según el contenido del HTML de la página.
        listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-qa="ad"]')))  # Cambié el selector
        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, 'h2[data-qa="ad-title"]').text  # Ajusté el selector al título del listado
                price = listing.find_element(By.CSS_SELECTOR, 'span[data-qa="ad-price"]').text  # Ajusté el selector al precio del listado
                titles.append(title)
                prices.append(price)
            except Exception as e:
                print(f"No se pudo extraer información de un listado: {e}")
    except Exception as e:
        print(f"No se pudieron encontrar los listados: {e}")

    # Verificar si se encontraron datos
    if not titles or not prices:
        print("No se encontraron datos. Verifica si el sitio web cambió su estructura.")
    else:
        # Crear el DataFrame con los datos extraídos
        data = pd.DataFrame({
            'Title': titles,
            'Price': prices
        })

        # Definir el camino donde se va a guardar el archivo CSV
        save_path = r'C:\Users\ney12\OneDrive\Desktop\plusvalia'

        # Crear el directorio si no existe
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Guardar los datos en un archivo CSV
        file_path = os.path.join(save_path, 'plusvalia_data.csv')
        data.to_csv(file_path, index=False)
        print(f"Datos guardados en {file_path}")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar el navegador
    driver.quit()
